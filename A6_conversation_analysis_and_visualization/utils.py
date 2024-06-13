import re
import pandas as pd
from bs4 import BeautifulSoup
import pdb 
stop = pdb.set_trace

def whatsapp2dataFrame(file_name: str, save_csv: bool = False):
    """Given a txt file of a whatsapp conversation, return a pandas dataframe with the following columns:
    date_time, sender, message, word_count, character_count, media_sent"""
    parsed_conversation = parse_whatsapp_conversation(file_name)
    df = pd.DataFrame(parsed_conversation[1:], columns=parsed_conversation[0])
    try:
        df["date_time"] = pd.to_datetime(df["date_time"], format="%m/%d/%y, %H:%M:%S")
    except ValueError:
        df["date_time"] = pd.to_datetime(df["date_time"], format="%d.%m.%y, %H:%M:%S")
    # df["word_count"] = df["message"].apply(count_words)
    # df["message_length"] = df["message"].apply(len)
    # df["time_diff_seconds"] = df["date_time"].diff().dt.total_seconds()
    # df["media_sent"] = df["message"].apply(check_media_sent)

    if save_csv:
        df.to_csv(f"data/{file_name.replace('.txt', '')}.csv", index=False)

    return df


def html2dataFrame(html_content : str, save_csv : bool = True) -> pd.DataFrame:

    soup = BeautifulSoup(html_content, "lxml")

    speech_blocks = soup.find_all(["a", "blockquote"])

    # Placeholder for the data
    data = []
    current_sender = None
    current_message = []

    for block in speech_blocks:
        if block.name == "a" and block.get("name") and block.b:
            # If it is a new sender
            if current_sender and current_message:
                data.append(
                    {
                        "date_time": len(data) + 1,
                        "sender": current_sender,
                        "message": " ".join(current_message),
                    }
                )
                current_message = []
            current_sender = block.b.text
        elif block.name == "blockquote" and current_sender:
            for tag in block.find_all("i"):
                tag.decompose()
            current_message.append(block.text.strip())
    if current_sender and current_message:
        data.append(
            {
                "date_time": len(data) + 1,
                "sender": current_sender,
                "message": " ".join(current_message),
            }
        )
    df = pd.DataFrame(data)
    if save_csv:
        df.to_csv(f"data/romeo_juliet_act2_scene2.csv", index=False)
    return df


def parse_whatsapp_conversation(file_path):
    """Take a whatsapp chat file and return a parsed version of the chat with separated columns for date, sender, and message."""
    # PART 1: Read the file
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # PART 2: Chunk the chat into individual messages
    # We'll use regex to see if a line is a new message or a continuation of the previous message. New messages start with the DATE_PATTERN. Then we'll chunk the chat into individual messages.
    DATE_PATTERN_US = r"\[\d{1,2}/\d{1,2}/\d{2}, \d{2}:\d{2}:\d{2}\]"

    DATE_PATTERN_EU = r"\[\d{2}.\d{2}.\d{2}, \d{2}:\d{2}:\d{2}\]"

    chunked_chat = []
    temporary_message = ""
    for line in lines:
        line = line.replace("\u200e", "") # Remove the left-to-right mark that appears in some messages
        if re.match(DATE_PATTERN_US, line) or re.match(DATE_PATTERN_EU, line):
            # The line we're looking at has a date. This means we have a new message. Save the previous temporary_message to the chunked_chat list and reset it so we can start a new message.
            if len(temporary_message) > 0:
                chunked_chat.append(temporary_message.strip())
            temporary_message = line.strip()
        else:
            # This is a continuation of the previous message. Append it to the temporary_message.
            temporary_message += line.strip() + " "

    # PART 3:Parse the chat into the base columns we want:date_str, sender, message
    parsed_chat = [["date_time", "sender", "message"]]
    DATE_PATTERN = re.compile(DATE_PATTERN_US + "|" + DATE_PATTERN_EU)

    for line in chunked_chat:
        date_str = re.match(DATE_PATTERN, line).group().strip("[]")
        content_chunk = line.split(date_str, 1)[1].strip()
        sender, msg = content_chunk.split(": ", 1)
        message = msg.replace("\n", " ").replace("  ", " ").strip()

        parsed_chat.append([date_str, sender.strip("] "), message])

    return parsed_chat

def count_emojis(message : str) -> int:
    """Count the number of emojis in a message, even if identical emojis are repeated."""
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u200d"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+"
    )
    counts = [len(elems) for elems in re.findall(EMOJI_PATTERN, message)]
    return sum(counts)


def check_media_sent(message):
    """Check if media was sent in a message."""
    MEDIA_TYPES = ["image", "video", "audio", "document", "gif", "sticker"]
    media_sent = "None"
    for medium in MEDIA_TYPES:
        if f"{medium} omitted" in message:
            media_sent = medium
    return media_sent


def test_import():
    """Method for testing that I got the library import correct."""
    print("File imported correctly")


def count_words(text):
    """Count the number of words in a provided string."""
    return len(text.split())


if __name__ == "__main__":
    convert_html_to_text("plays/romeo_juliet_act3_scene5.html", save_csv=True)
    convert_html_to_text("plays/romeo_juliet_act2_scene2.html", save_csv=True)
    convert_html_to_text("plays/hamlet_act3_scene4.html", save_csv=True)
    convert_html_to_text("plays/hamlet_act1_scene2.html", save_csv=True)
