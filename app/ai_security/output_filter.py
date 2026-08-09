class OutputFilter:


    BLOCKED_OUTPUTS = [

        "api_key",

        "password",

        "secret",

        "private key",

    ]



    def validate(

        self,

        response: str,

    ) -> str:


        lower = response.lower()


        for item in self.BLOCKED_OUTPUTS:


            if item in lower:


                raise ValueError(

                    "Sensitive information detected."

                )


        return response