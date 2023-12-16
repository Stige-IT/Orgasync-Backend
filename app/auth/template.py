def template_body(code: int) -> str:
    template = """
                <html>
                    <body>
                        <h1>ORGASYNC CORP</h1>
                        <p>Hi !!!</p>
                        <br>
                        <p>Thanks for using orgasync app, keep using it..!!!</p>
                        <br>
                        <p>Here is your verification code:</p>
                        <br>
                        <h2>""" + str(code) + """</h2>
                    </body>
                </html>
                """
    return template
