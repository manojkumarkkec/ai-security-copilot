from pypdf import PdfReader

import io



class PDFParser:


    def parse(

        self,

        content: bytes,

    ) -> str:


        reader = PdfReader(

            io.BytesIO(content)

        )


        text = ""


        for page in reader.pages:

            text += page.extract_text() or ""


        return text