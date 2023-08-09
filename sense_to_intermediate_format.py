import sys
import os
from zipfile import ZipFile
from io import StringIO
import json


def build_ground_truth_string(image_path, text, buffer: StringIO):
    _template = "{image_path}\t{text}\n"
    buffer.write(_template.format(image_path=image_path, text=text))


def main(dataset_path, output_dir):
    with ZipFile(dataset_path, "r") as zf:
        for file in zf.namelist():
            if not file.endswith(".json"):
                continue
            buf = StringIO()
            split = os.path.basename(file).split(".")[0]
            labels = json.load(zf.open(file))["labels"]
            for label in labels:
                try:
                    gt = label["annotations"]["Tattoo"]["data"]
                except:
                    continue
                gt = gt.strip().upper().replace(" ", "").replace("5", "X").replace("Z", "2")

                if len(gt) < 4 or len(gt) > 4:
                    print(gt)
                    continue

                image_path = label["path"]
                output_image_path = os.path.join(output_dir, split, os.path.basename(image_path))
                build_ground_truth_string(os.path.join(split, os.path.basename(image_path)), gt, buf)
                with open(output_image_path, "wb") as fp:
                    fp.write(zf.open(image_path).read())

            with open(os.path.join(output_dir, f"{split}.txt"), "w") as fp:
                fp.write(buf.getvalue())


if __name__ == "__main__":
    try:
        dataset_path = sys.argv[1]
    except:
        raise ValueError("Supply a path to a sense dataset")

    output_dir = os.path.join("dataset", os.path.basename(dataset_path).split(".")[0])
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "train"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "validation"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "test"), exist_ok=True)
    main(dataset_path, output_dir)
