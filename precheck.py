import argparse
import text
import os
from utils import load_filepaths_and_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_extension", default="cleaned")
    parser.add_argument("--text_index", default=1, type=int)
    parser.add_argument(
        "--filelists",
        nargs="+",
        default=[
            "filelists/ljs_audio_text_val_filelist.txt",
            "filelists/ljs_audio_text_test_filelist.txt",
        ],
    )
    parser.add_argument("--text_cleaners", nargs="+", default=["english_cleaners2"])

    args = parser.parse_args()

    for filelist in args.filelists:
        print("START:", filelist)
        filepaths_and_text = load_filepaths_and_text(filelist)
        for i in range(len(filepaths_and_text)):
            if os.path.exists(f"/home/circulus/TTS/{filepaths_and_text[i][0]}") is False:
                print(filepaths_and_text[i][0])
            if os.path.getsize(f"/home/circulus/TTS/{filepaths_and_text[i][0]}") < 100:
                print(filepaths_and_text[i][0])                
            #original_text = filepaths_and_text[i][args.text_index]
            #cleaned_text = text._clean_text(original_text, args.text_cleaners)
            #filepaths_and_text[i][args.text_index] = cleaned_text
            #filepaths_and_text[i][0] = f"/home/circulus/TTS/{filepaths_and_text[i][0]}" 
            #print(i,filepaths_and_text[i])

        #new_filelist = filelist + "." + args.out_extension
        #with open(new_filelist, "w", encoding="utf-8") as f:
            #f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])
