from phi.agent import Agent
from phi.model.google import Gemini
from phi.workflow import Workflow, RunResponse, RunEvent

from .modules.llama_ocr import image_to_md
from .modules.preprocess_image import preprocess_image, save_image, load_image
from .models import *
from .prompts import *

import json
import logging
import numpy as np
from PIL import Image
from typing import Iterator

logger = logging.getLogger(__name__)


class Processor(Workflow):
    file: str = None
    markdown: str = None
    image: np.ndarray = None
    data: Data = None

    validator: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        instructions=VALIDATOR_INSTRUCTIONS.splitlines(),
        markdown=False,
    )

    formatter: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        instructions=FORMATTER_INSTRUCTIONS.splitlines(),
        markdown=True,
    )

    extractor: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        instructions=EXTRACTOR_INSTRUCTIONS.splitlines(),
        markdown=True,
    )

    converter: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        instructions=CONVERTER_INSTRUCTIONS.splitlines(),
        markdown=False,
        output_model=Data,
        structured_outputs=True,
    )

    def run(self, file: str = None, markdown: str = None) -> Iterator[RunResponse]:
        try:
            self.process(file=file, markdown=markdown)
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            yield RunResponse(
                event=RunEvent.workflow_completed,
                content=f"Error processing image",
            )
            return
        try:
            formatted_markdown = self.formatter.run(f"""{FORMATTER_PROMPT.replace("{input_markdown}", f"{self.markdown}")}""")
            logger.info("Markdown formatted")
            logger.debug(f"Formatted markdown:\n {formatted_markdown.content}")
            extracted_markdown = self.extractor.run(f"""{EXTRACTOR_PROMPT.replace("{formatted_markdown}", f"{formatted_markdown.content}")}""")
            logger.info("Markdown extracted")
            logger.debug(f"Extracted markdown:\n {extracted_markdown.content}")
            data = self.converter.run(f"""{CONVERTER_PROMPT.replace("{extracted_markdown}", f"{extracted_markdown.content}")}""")
            logger.info("Markdown converted to data")
            yield RunResponse(content=json.dumps(data.model_dump(), indent=2), event=RunEvent.workflow_completed)
            return
        except Exception as e:
            logger.error(f"Error converting markdown to data: {e}")
            yield RunResponse(
                event=RunEvent.workflow_completed,
                content=f"Error converting markdown to data",
            )
            return

    def process(self, file: str = None, markdown: str = None) -> None:
        if file:
            self.file = file
            self.image = load_image(file)
            image_path = file

            if self.image is not None:
                preprocessed_image = preprocess_image(file)
                if not isinstance(preprocessed_image, np.ndarray):
                    logger.error("Preprocessed image returned funky")
                    raise ValueError("Preprocessed image is not a valid NumPy array")
                self.validator.add_image(Image.fromarray(preprocessed_image))
                valid_image = self.validator.run()
                if valid_image == "valid":
                    logger.info("Preprocessed image is valid. Using preprocessed image")
                    self.image = preprocessed_image
                    image_path = "data/new_processed_image.jpg"
                    save_image(preprocessed_image, image_path)
                else:
                    logger.info("Preprocessed image is invalid. Using original image")
            self.markdown = image_to_md(image_path)
            logger.info("Image converted to markdown")
            logger.info(f"Markdown:\n {self.markdown}")
            return
        elif markdown:
            self.markdown = markdown
            logger.info("Markdown loaded")
            return
        else:
            logger.error("No file or markdown provided")
            return
