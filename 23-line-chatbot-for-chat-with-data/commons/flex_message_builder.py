from linebot.v3.messaging import (
    ReplyMessageRequest,
    TextMessage,
    FlexContainer,
    FlexMessage,
    FlexCarousel,
    QuickReply,
    QuickReplyItem,
    MessageAction,
    LocationAction,
)


def build_flex_carousel_message(
    line_bot_api, event, response_dict, search_query, additional_explain=None
):
    result_products_list = []
    product_bubble_temple = open("templates/flex_product_bubble.json").read()
    summary_text = response_dict["summary"]["summaryText"]
    
    for idx, result in enumerate(response_dict["results"]):
        product_name = result["document"]["structData"]["name"]
        product_price = result["document"]["structData"]["price"]
        product_image_url = result["document"]["structData"]["image_url"]
        product_sku = result["document"]["structData"]["sku"]

        product_bubble_json = (
            product_bubble_temple.replace("<PRODUCT_NAME>", product_name)
            .replace("<PRODUCT_PRICE>", str(product_price))
            .replace("<PRODUCT_IMAGE_URL>", product_image_url)
            .replace("<PRODUCT_SKU>", str(product_sku))
            .replace("<PRODUCT_NUMBER>", str(idx + 1))
        )

        result_products_list.append(FlexContainer.from_json(product_bubble_json))

    carousel_flex_message = FlexMessage(
        alt_text=f"ผลการค้นหาสินค้า: {search_query}",
        contents=FlexCarousel(
            type="carousel",
            contents=result_products_list,
        ),
    )

    messages_list = [
        TextMessage(text=summary_text),
        carousel_flex_message,
        TextMessage(
            text="คุณสามารถกดเพิ่มสินค้าในตระกร้าได้ สอบถามเกี่ยวกับสินค้าอื่นได้ หรือค้นหาสาขาใกล้เคียงได้เลยค่ะ",
            quick_reply=QuickReply(
                items=[
                    QuickReplyItem(
                        action=MessageAction(
                            label="คุยกับน้อง CJ", text="คุยกับน้อง CJ"
                        )
                    ),
                    QuickReplyItem(action=LocationAction(label="ค้นหาสาขาใกล้เคียง")),
                ]
            ),
        ),
    ]
    if additional_explain:
        messages_list.insert(0, TextMessage(text=additional_explain))

    line_bot_api.reply_message(
        ReplyMessageRequest(reply_token=event.reply_token, messages=messages_list)
    )
