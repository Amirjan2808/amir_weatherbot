from googletrans import Translator

translater = Translator()

API_TOKEN = "5245421544:AAH8KJL3QaJxSSEfuBU1ysI0W3HpfHa5J0c"

code_smiles_uz = {
    "Clear": "Toza \U00002600",
    "Clouds": "Bulutli \U00002601",
    "Rain": "Yomg`ir \U00002614",
    "Drizzle": "Yomg`ir \U00002614",
    "Thunderstorm": "Chaqmoq \U000026A1",
    "Snow": "Qor \U0001F328",
    "Mist": "Tuman \U0001F32B"
}

code_smiles_ru = {
    "Clear": f"{translater.translate('Toza', 'ru').text} \U00002600",
    "Clouds": f"{translater.translate('Bulutli', 'ru').text} \U00002601",
    "Rain": f"{translater.translate('Yomg`ir', 'ru').text} \U00002614",
    "Drizzle": f"{translater.translate('Yomg`ir', 'ru').text} \U00002614",
    "Thunderstorm": f"{translater.translate('Chaqmoq', 'ru').text} \U000026A1",
    "Snow": f"{translater.translate('Qor', 'ru').text} \U0001F328",
    "Mist": f"{translater.translate('Tuman', 'ru').text} \U0001F32B"
}

API_KEY = "aeff74af7fec2b68fb196a72a6e458f1"