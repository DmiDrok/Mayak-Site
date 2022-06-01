html_text = """
    <html>
        <head>
            <style>
                .content_here{
                    width: 100%;
                    background-color: #24c0a7;
                    border-radius: 5px;
                    padding: 1rem 2rem;
                    font-family: Tahoma;
                }

                .content_here{
                    color: #fff;
                }

                .content_text{
                    padding-left: 1.5rem;
                    max-width: 665px;
                }

                .content_text pre{
                    font-size: 16px;
                }

                #telefon, #email, #email a{
                    text-decoration: underline;
                    color: #fff;
                }

                #email a:hover{
                    color: #dbdbdb;
                }
            </style>
        </head>

        <body>
            <div class="content_here">
                <h1>
                    {{subject}}
                </h1>

                <div class="content_text">
                    <h3 id="telefon">
                        Телефон: {{telefon}}
                    </h3>

                    <h3 id="email">
                        Почта: {{email}}
                    </h3>

                    <h3>
                        Описание проблемы:
                        <br/>
                    </h3>

                    <pre>
{{content}}
                    </pre>
                </div>
            </div>
        </body>
    </html>
"""