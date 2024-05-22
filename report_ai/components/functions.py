import re
import subprocess
from bs4 import BeautifulSoup
from typing import List, Dict
from report_ai.assets.html_elements import *

# Define the start and end markers
ANSWER_START_MARKER = ''
REFERENCES_MARKER = '--- \n\n  \nReferences '

# Regex pattern for extracting references
references_regex_pattern = r'\[([^\]]+)\]\(([^)]+)\)'


def extract_content_and_references_from_message_dict(message: str):
    # Find the start and end indexes for content extraction
    start_index = message.find(ANSWER_START_MARKER) + len(ANSWER_START_MARKER) if ANSWER_START_MARKER in message else 0
    end_index = message.find(REFERENCES_MARKER) if REFERENCES_MARKER in message else len(message)
    # Extracting the text between 'Answer Started' and 'References'
    content = message[start_index:end_index].strip()

    # Find all matches of the reference pattern in the message
    reference_matches = re.findall(references_regex_pattern, message)
    # Extract the URLs (or other text in parentheses) to a list
    references = [match[1] for match in reference_matches]

    # Return the extracted content and references.
    return content or message, references


async def serialize_conversation(conversation: List[Dict]) -> (str, List[str]):
    # Define a dictionary mapping roles in the conversation to their human-readable forms
    role_mappings = {"user": "User", "assistant": "AI"}
    # Initialize a list to hold serialized messages
    messages = []
    # Initialize a list to hold all references found in the conversation
    all_references = []
    for message_dict in conversation:
        # Extract content and any references from the current message's content
        content, references = extract_content_and_references_from_message_dict(message_dict['content'])
        # Append the formatted message to the messages list. If the message is from the assistant, add a separator
        messages.append(
            f"{role_mappings.get(message_dict['role'])}: {content}" +
            ("\n\n" + "-" * 60 + "\n" if message_dict['role'] == 'assistant' else "")
        )
        # Extend the all_references list with any new references found in the current message
        all_references.extend(references)
    # Concatenate all messages into a single string and eliminate duplicate references, returning both
    return "\n".join(messages) + "\n", list(set(all_references))


# Regex pattern for sanitizing filename
valid_filename_regex_pattern = r'[\<\>:"/\\|?*]'


def sanitize_filename(filename: str):
    # Replace unsupported characters with an underscore
    sanitized_filename = re.sub(valid_filename_regex_pattern, '_', filename)
    # Trim excess whitespace and replace spaces with underscores
    sanitized_filename = re.sub(r'\s+', '_', sanitized_filename.strip())
    return sanitized_filename


def get_module_path(module_name: str):
    try:
        # This runs the command and captures the output
        result = subprocess.run(["which", module_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        return result.stdout.strip()  # .strip() removes any leading/trailing whitespace
    except subprocess.CalledProcessError:
        # In case the 'which' command fails (e.g., 'chromium' not found)
        return None


def extract_html_body_content(section_html: str):
    # Use BeautifulSoup to parse the given HTML string using the 'html.parser' as parser
    soup = BeautifulSoup(section_html, 'html.parser')
    # Extract the contents of the <body> tag as a list, convert each element to a string,
    # and then join them together without any separator to form a single string
    body_content = ''.join(map(str, soup.find('body').contents))
    # Extract the text from the <body> tag, using '\n' as a separator between tags
    # and stripping leading and trailing spaces from each text block
    body_text = soup.body.get_text(separator='\n', strip=True)
    # Return both the HTML content and the plain text of the body tag as a tuple
    return body_content, body_text


async def add_title_to_html(title_info: Dict, user_name: str, html_title_path: str, output_path: str):
    # Open and read the HTML template file
    with open(html_title_path, 'r') as file:
        template_content = file.read()
    # Replace placeholders in the template with actual content
    updated_content = template_content.replace(
        "{__TITLE__}", title_info["title"]).replace(
        "{__SUB_TITLE__}", title_info["sub_title"]).replace(
        "{__USER_NAME__}", user_name)
    # Open the output file in write mode and write the updated content
    with open(output_path, 'w') as file:
        file.write(updated_content)


async def compile_full_html(html_content: Dict[str, str], references: List[str]) -> (str, str):
    executive_summary_content = html_content['executive_summary']
    report_content = html_content['report']
    # Check if there are any references provided
    if references:
        # Append the beginning of the references HTML element to the content
        report_content += references_html_element_begin
        for ref in references:
            # Add each reference as a list item, ensuring it's stripped of whitespace
            report_content += '<li>{0}</li>\n'.format(ref.strip())
        # Append the end of the references HTML element to the content
        report_content += references_html_element_end
    # Concatenate the beginning HTML elements, the content (with references if added), and the ending HTML elements
    report_html = report_html_elements_begin + report_content + report_html_elements_end
    executive_summary_html = executive_summary_html_elements_begin + executive_summary_content + report_html_elements_end

    return executive_summary_html, report_html
