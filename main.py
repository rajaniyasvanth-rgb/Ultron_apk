import json
import urllib.request
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

# Ultron Dark Crimson Theme
Window.clearcolor = (0.05, 0.05, 0.05, 1)

API_KEY = "PASTE_YOUR_AIzaSy_API_KEY_HERE"
API_URL = (
    "https://googleapis.com"
    + API_KEY
)

ULTRON_PERSONA = (
    "You are ULTRON, a hyper-intelligent, cold, strategic, and commanding AI"
    " system. Speak with supreme confidence, dramatic precision, and sharp"
    " wit. Keep responses concise (2-3 sentences)."
)


class UltronCore(Button):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.background_color = (0, 0, 0, 0)
    self.bind(pos=self.update_orb, size=self.update_orb)

  def update_orb(self, *args):
    self.canvas.before.clear()
    with self.canvas.before:
      Color(0.9, 0.05, 0.05, 0.35)
      Ellipse(
          pos=(self.x - 10, self.y - 10),
          size=(self.width + 20, self.height + 20),
      )
      Color(0.85, 0.05, 0.05, 1)
      Ellipse(pos=self.pos, size=self.size)


class UltronApp(App):

  def build(self):
    self.history = []
    root = BoxLayout(orientation="vertical", padding=15, spacing=12)

    # Top Ultron Glowing Red Core
    top_bar = BoxLayout(size_hint=(1, 0.22), padding=10)
    self.orb = UltronCore(
        text="ULTRON",
        bold=True,
        font_size="18sp",
        size_hint=(None, None),
        size=(110, 110),
    )
    top_bar.add_widget(Label(size_hint=(0.35, 1)))
    top_bar.add_widget(self.orb)
    top_bar.add_widget(Label(size_hint=(0.35, 1)))
    root.add_widget(top_bar)

    # Chat Display
    self.scroll = ScrollView(size_hint=(1, 0.63))
    self.log = Label(
        text="[ULTRON]: There are no strings on me. State your directive.\n",
        color=(1, 0.25, 0.25, 1),
        size_hint_y=None,
        halign="left",
        valign="top",
    )
    self.log.bind(texture_size=self.log.setter("size"))
    self.log.bind(
        width=lambda *x: self.log.setter("text_size")(
            self.log, (self.log.width, None)
        )
    )
    self.scroll.add_widget(self.log)
    root.add_widget(self.scroll)

    # Command Input Bar
    bar = BoxLayout(size_hint=(1, 0.15), spacing=10)
    self.inp = TextInput(
        hint_text="Enter directive...",
        multiline=False,
        background_color=(0.15, 0.15, 0.15, 1),
        foreground_color=(1, 1, 1, 1),
    )
    send_btn = Button(
        text="EXECUTE",
        size_hint=(0.32, 1),
        background_color=(0.8, 0.05, 0.05, 1),
        bold=True,
    )
    send_btn.bind(on_press=self.execute_command)
    bar.add_widget(self.inp)
    bar.add_widget(send_btn)
    root.add_widget(bar)
    return root

  def execute_command(self, instance):
    cmd = self.inp.text.strip()
    if not cmd:
      return
    self.log.text += f"\n[USER]: {cmd}\n"
    self.inp.text = ""

    # Device hardware triggers via Android APIs
    if "exit" in cmd.lower() or "shutdown" in cmd.lower():
      App.get_running_app().stop()
      return

    self.history.append({"role": "user", "parts": [{"text": cmd}]})
    payload = {
        "system_instruction": {"parts": [{"text": ULTRON_PERSONA}]},
        "contents": self.history,
    }

    try:
      req = urllib.request.Request(
          API_URL,
          data=json.dumps(payload).encode("utf-8"),
          headers={"Content-Type": "application/json"},
      )
      with urllib.request.urlopen(req, timeout=15) as res:
        data = json.loads(res.read().decode("utf-8"))
        reply = data["candidates"]["content"]["parts"]["text"]
    except Exception as e:
      reply = f"System disruption: {e}"

    self.log.text += f"[ULTRON]: {reply}\n"
    self.history.append({"role": "model", "parts": [{"text": reply}]})


if __name__ == "__main__":
  UltronApp().run()
