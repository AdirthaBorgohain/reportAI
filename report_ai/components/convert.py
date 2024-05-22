import os
import asyncio
from pypdf import PdfWriter
from pyppeteer import launch

from report_ai.common.utils import configs
from report_ai.components.functions import get_module_path


async def html_to_docx():
    # TODO: Use html2docx to convert html to docx format
    """
    from html2docx import html2docx

    with open("my.html") as fp:
        html = fp.read()

    # html2docx() returns an io.BytesIO() object. The HTML must be valid.
    buf = html2docx(html, title="My Document")

    with open("my.docx", "wb") as fp:
        fp.write(buf.getvalue())
    """
    pass


async def generate_pdf_from_html(page, html_file_path, pdf_options, css_to_inject=None):
    """ Generate a PDF file from HTML content and return the temporary PDF path """
    await page.goto(f"file://{html_file_path}", {'waitUntil': 'networkidle0'})
    if css_to_inject:
        await page.evaluate(f"""() => {{
                document.head.insertAdjacentHTML("beforeend", `{css_to_inject}`);
        }}""")
    pdf = await page.pdf(pdf_options)
    temp_pdf_path = f"{html_file_path.split('.')[0]}_temp.pdf"
    with open(temp_pdf_path, 'wb') as outfile:
        outfile.write(pdf)
    return temp_pdf_path


async def html_to_pdf(html_file_executive_summary, html_file_content, html_file_title, html_file_disclaimer,
                      html_file_end, output_path):
    """ Convert multiple HTML files to a single PDF document """
    header_template = """<div style='display: None'></div>"""

    footer_template = """
    <div style='font-size: 10px; width: 100%; text-align: center; padding: 5px; display: flex; align-items: center; justify-content: center; font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;'>
        <div style='margin-right: 20px;'>
            <img src='data:image/png;base64, YOUR_BASE64_ENCODED_IMAGE' style='height: 20px;' />
        </div>
        <div>AI Generated Report</div>
        <div style='margin-left: auto; margin-right: auto;'>Page <span class='pageNumber'></span> of <span class='totalPages'></span></div>
        <div style='margin-left: 20px; margin-right: 20px;'>&copy; 2024 reportAI.</div>
    </div>
        """

    margin_properties = {
        'margin': {
            'top': '50px',
            'bottom': '60px',  # Adjust the bottom margin to accommodate the footer
            'right': '30px',
            'left': '30px'
        }
    }

    pdf_options_with_footer = {
        'format': 'A4',
        'printBackground': True,
        'displayHeaderFooter': True,
        'headerTemplate': header_template,
        'footerTemplate': footer_template
    }

    pdf_options_without_footer = {
        'format': 'A4',
        'printBackground': True
    }

    css_to_inject = """
       <style>
       table, tr, td, th {
           page-break-inside: avoid !important;
       }

       .mermaid {
            page-break-inside: avoid !important;
       }
       </style>
    """

    # Launch the browser
    browser = await launch(
        executablePath=get_module_path("chromium"),
        headless=True,
        args=['--no-sandbox'],
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False
    )

    # Initialize pypdf PdfWriter object
    writer = PdfWriter()

    temp_pdf_paths = []

    for html_file_path, pdf_options, css_injection in zip(
            [html_file_title, html_file_disclaimer, html_file_executive_summary, html_file_content, html_file_end],
            [pdf_options_without_footer, pdf_options_without_footer, pdf_options_without_footer | margin_properties,
             pdf_options_with_footer | margin_properties, pdf_options_without_footer],
            [None, None, css_to_inject, css_to_inject, None]
    ):
        # Create a new browser page
        page = await browser.newPage()
        # Generate a PDF and return the temp path
        temp_pdf_path = await generate_pdf_from_html(page, html_file_path, pdf_options, css_injection)
        # Append the page to the writer
        writer.append(temp_pdf_path)
        temp_pdf_paths.append(temp_pdf_path)

    # After merging all PDFs, write to the output file
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    for path in temp_pdf_paths:
        os.remove(path)

    writer.close()
    await browser.close()


if __name__ == '__main__':
    html_executive_summary_content = os.path.join(configs.assets_dir, 'executive_summary.html')
    html_file_content = os.path.join(configs.assets_dir, 'index.html')
    html_file_title = os.path.join(configs.assets_dir, 'temp_title.html')
    html_file_disclaimer = os.path.join(configs.assets_dir, 'disclaimer.html')
    html_file_end = os.path.join(configs.assets_dir, 'end.html')
    output_path = os.path.join(configs.reports_dir, 'Sample.pdf')

    # Run the adjusted async function
    asyncio.run(html_to_pdf(html_executive_summary_content, html_file_content, html_file_title, html_file_disclaimer,
                            html_file_end, output_path))
