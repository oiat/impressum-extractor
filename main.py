import json

from services.impressum_extractor import ImpressumExtractor
from utils.args import parse_args
from utils.settings import settings

if __name__ == "__main__":

    extractor = ImpressumExtractor(
        api_key=settings.gemini.api_key,
        prompt_path=settings.impressum.prompt_path,
        schema_path=settings.impressum.scheme_path,
    )

    args = parse_args()

    if not args.url:
        raise quit("No url provided")

    result = extractor.run(args.url)

    with open(settings.impressum.output_path, "w") as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False))
