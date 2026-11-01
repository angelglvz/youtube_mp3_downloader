# 🤖 Django Telegram YouTube MP3 Bot

A robust, webhook-driven Telegram bot built with **Django** and **Python**. It processes incoming chat updates securely and integrates with **`yt-dlp`** and **FFmpeg** to extract, convert, and send YouTube videos directly as playable MP3 audio files to your Telegram chat.

## 🚀 Features
* **Webhook Architecture:** Secure, CSRF-exempt endpoint handling Telegram updates in real-time.
* **YouTube to MP3 Conversion:** Automatically downloads audio streams using `yt-dlp` and processes them via FFmpeg.
* **Direct Audio Delivery:** Sends processed `.mp3` files straight to the conversation using Telegram's `sendAudio` API.
* **Local Development Ready:** Seamless integration with tunneling tools like Localtunnel for instant testing.