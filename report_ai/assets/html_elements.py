executive_summary_html_elements_begin = '''
<!DOCTYPE html>
<html>
    <head>
       <title>reportAI</title>
       <style>
          body {
              font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
              font-size: 12px;
              color: #333;
              line-height: 1.6;
              padding: 30px 20px;
              max-width: 800px;
              text-align: justify;
          }
          /* Heading styles */
          h1 {
              font-size: 1.75em;
              color: #000000;
          }
          h2 {
              text-align: center;
              margin-top: 20px;
              margin-bottom: 9px;
              font-size: 1.5em;
              border-bottom: 2px solid #eee;
              padding-bottom: 5px;
              color: #FF5757;
          }
          h3 {
              margin-top: 18px;
              margin-bottom: 7px;
              font-size: 1.10em;
              color: #000000;
          }
          /* Paragraph styles */
          p {
              margin-top: 0;
              margin-bottom: 1em;
          }
          ul {
              line-height: 1.6; /* Enhances readability by increasing line spacing */
              color: #333; /* Dark grey text for better readability */
          }
          /* Styling individual list items */
          li {
              margin-bottom: 5px; /* Adds space between list items */
              padding-left: 10px; /* Padding inside each list item */
          }
          /* Enhance the appearance of key terms such as 'Ulcerative Colitis' */
          li strong {
              color: #ba2727;; /* Red color for key terms */
              font-weight: bold; /* Makes key terms bold */
          }
          .mermaid {
              letter-spacing: 0.5px;
              padding-left: 50px; /* Padding around the content */
              border-radius: 8px; /* Rounded corners */
              font-family: 'Arial', sans-serif; /* Font styling */
              color: #333; /* Dark grey text color */
              text-align: center; /* Center the text */
          }
          a {
              color: #0056b3;
              text-decoration: none;
          }
          table {
              width: 100%;
              margin-top: 20px;
              margin-bottom: 20px;
              border-collapse: collapse;
          }
          table,
          th,
          td {
            border: 1px solid #ddd; /* Lighter border color */
          }
          th,
          td {
            text-align: left;
            padding: 8px;
          }
          /* Introducing more pronounced colors */
          th {
              background-color: #212121; /* Black for header cells */
              color: #ffffff; /* White text for contrast */
          }
          tr:nth-child(even) {
            background-color: #f2f2f2; /* Lighter gray for even rows */
          }
          tr:nth-child(odd) {
            background-color: #ffffff; /* Keeping odd rows white for cleanliness */
          }
          /* Addition: Table caption style with adjusted color for emphasis */
          caption {
              margin-top: 20px;
              margin-bottom: 10px;
              font-size: 1.2em;
              font-weight: bold;
              text-align: left;
              color: #FF5757; /* Echoing the vibrant red for cohesion */
          }
          @media print {
            .pagebreak {
                clear: both;
                page-break-after: always;
            }
          }
       </style>
        <script type="module">
            import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
        </script>
    </head>
    <body>
'''
report_html_elements_begin = '''
<!DOCTYPE html>
<html>
    <head>
        <title>reportAI</title>
        <style>
            body {
                font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 12px;
                color: #333;
                line-height: 1.6;
                margin: 0;
                padding: 0 20px;
                max-width: 800px;
                margin: auto;
                text-align: justify;
            }

            /* Heading styles */

            h1 {
                margin-top: 22px;
                margin-bottom: 10px;
                font-size: 1.75em;
                color: #000000; 
            }

            h2 {
                margin-top: 20px;
                margin-bottom: 9px;
                font-size: 1.5em;
                border-bottom: 2px solid #eee;
                padding-bottom: 5px;
                color: #FF5757;
            }

            h3 {
                margin-top: 18px;
                margin-bottom: 7px;
                font-size: 1.10em;
                color: #000000;
            }

            /* Paragraph styles */
            p {
                margin-top: 0;
                margin-bottom: 1em;
            }

            /* List styles */
            ul {
                margin-top: 0;
                margin-bottom: 1em;
            }

            ul li {
                line-height: 1.6;
            }

            /* Link styles */
            a {
                color: #0056b3;
                text-decoration: none;
            }

            table {
                width: 100%;
                margin-top: 20px;
                margin-bottom: 20px;
                border-collapse: collapse;
            }

            table,
            th,
            td {
                border: 1px solid #ddd; /* Lighter border color */
            }

            th,
            td {
                text-align: left;
                padding: 8px;
            }

            /* Introducing more pronounced colors */
            th {
                background-color: #212121; /* Vibrant red for header cells */
                color: #ffffff; /* White text for contrast */
            }

            tr:nth-child(even) {
                background-color: #f2f2f2; /* Lighter gray for even rows */
            }

            tr:nth-child(odd) {
                background-color: #ffffff; /* Keeping odd rows white for cleanliness */
            }
            
            .mermaid {
                text-align: center;
            }
            
            /* Addition: Table caption style with adjusted color for emphasis */
            caption {
                margin-top: 20px;
                margin-bottom: 10px;
                font-size: 1.2em;
                font-weight: bold;
                text-align: left;
                color: #FF5757; /* Echoing the vibrant red for cohesion */
            }
            .references {
                margin: 20px 0;
            }
            .reference-list {
                counter-reset: reference-counter;
                list-style: none;
                padding-left: 0;
            }
            .reference-list li {
                display: flex; /* This creates a flex container */
                align-items: baseline; /* Aligns items on their baseline */
                margin-bottom: 3px;
                counter-increment: reference-counter;
            }
            .reference-list li::before {
                content: counter(reference-counter) ". ";
                font-weight: bold;
                margin-right: 5px; /* Adds some space between the number and the text */
                /* Prevents the number from taking up more space than necessary */
                flex-shrink: 0;
            }
            @media print {
                .pagebreak {
                    clear: both;
                    page-break-after: always;
                }
            }
        </style>
        <script type="module">
            import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
        </script>
    </head>
    <body>
'''

report_html_elements_end = '''
    </body>
</html>
'''

references_html_element_begin = '''
<div class="pagebreak"></div>
<h2>References</h2>
<div class="references">
    <ol class="reference-list">
'''

references_html_element_end = '''
    </ol>
</div>
'''

__all__ = ['executive_summary_html_elements_begin', 'report_html_elements_begin', 'report_html_elements_end',
           'references_html_element_begin', 'references_html_element_end']
