import ptbot
from pytimeparse import parse
from decouple import config

TG_TOKEN = config('TG_TOKEN')


def render_progressbar(total, iteration, prefix='', suffix='', length=30,
                       fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(seconds_left, chat_id, message_id, total_seconds, bot):
    progress = total_seconds - seconds_left
    bot.update_message(
          chat_id,
          message_id,
          f"{seconds_left}s left\n"
          f"{render_progressbar(total_seconds, progress)}"
        )


def get_answer(chat_id, question, bot):
    bot.send_message(chat_id, f"Time's up!, {question}")


def wait(chat_id, question, bot):
    seconds = parse(question)
    if seconds is None:
        bot.send_message(
            chat_id,
            "Couldn't parse the time. Try: 10s, 2m, 1h, etc."
        )
        return

    message_id = bot.send_message(
        chat_id,
        f"{seconds}s left \n{render_progressbar(seconds, 0)}"
    )

    bot.create_countdown(
        seconds,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        total_seconds=seconds,
        bot=bot
    )

    bot.create_timer(
        seconds,
        get_answer,
        chat_id=chat_id,
        question=question,
        bot=bot
    )


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(wait, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
