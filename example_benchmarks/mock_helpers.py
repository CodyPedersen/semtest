"""Mock helper functions"""
from typing import Generator

def mock_llm_response_prompt1() -> Generator[str, None, None]:
    """Mocks a quality llm response"""
    yield from [
        "There's a dog in the background of the photo",
        "In the background of the photo is a dog",
        "There's an animal in the background of the photo and it's a dog."
    ]

def mock_llm_response_prompt2() -> Generator[str, None, None]:
    """Mocks a slightly lower quality llm response"""
    yield from  [
        "In the background of the photograph there is a furry animal",
        "In the foreground there is a human, and I see a dog in the background of the photograph",
        "There are two dogs in the background of the image"
    ]
