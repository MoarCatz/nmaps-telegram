from uuid import uuid4

from telegram import (InlineQueryResultArticle, InputTextMessageContent, Bot,
                      Update)
from telegram.ext import InlineQueryHandler

from bot.config import indices
from bot.phrases import inline_templates, INLINE_HELP_BUTTON


def inline_search(_bot: Bot, update: Update) -> None:
    query = update.inline_query

    search_results = []
    for index in indices:
        search_results.append((index.name, index.search(query.query)))

    articles = []
    for index in search_results:
        for res in index[1]["hits"]:
            args_list = inline_templates[index[0]]["args"]
            args = [res[arg] for arg in args_list]

            message_text = InputTextMessageContent(
                message_text=inline_templates[index[0]]["text"].format(*args),
                parse_mode="html",
            )
            articles.append(
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=res["title"],
                    url=res["url"] if "url" in res else None,
                    description=res["short"] if "short" in res
                    else res["text"],
                    input_message_content=message_text,
                    hide_url=True,
                )
            )
    query.answer(
        articles,
        switch_pm_text=INLINE_HELP_BUTTON,
        switch_pm_parameter="inline-help",
        cache_time=0,
    )


inline_search_handler = InlineQueryHandler(inline_search)
