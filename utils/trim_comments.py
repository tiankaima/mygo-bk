import os
import json

comment_path = "./export"
export_trimmed_comment_path = "../assets/json/"


def trim_comment(comment: dict) -> dict:
    comment_new = {}
    comment_new["author_name"] = comment["member"]["uname"]
    comment_new["author_id"] = comment["member"]["mid"]
    comment_new["time"] = comment["ctime"]
    comment_new["content"] = comment["content"]["message"]
    comment_new["like"] = comment["like"]
    return comment_new


def trim_file(name: str) -> None:
    input_file = comment_path + "/" + name
    if len(name) == 6:
        name = "0" + name
    output_file = export_trimmed_comment_path + name

    with open(input_file, "r") as f:
        data = json.load(f)

    data_new = []
    for comment in data:
        comment_new = trim_comment(comment)
        replies = []
        for reply in comment["replies"]:
            reply_new = trim_comment(reply)
            replies.append(reply_new)
        comment_new["replies"] = replies
        data_new.append(comment_new)

    with open(output_file, "w") as f:
        json.dump(data_new, f, ensure_ascii=False, indent=None)


def main():
    for file in os.listdir(comment_path):
        try:
            trim_file(file)
        except Exception as e:
            print(file)
            print(e)


if __name__ == "__main__":
    main()
