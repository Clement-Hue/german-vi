from game import Game
from window import Window

if __name__ == '__main__':
   tries = input("Number of try: ")
   game = Game(int(tries))
   word, form = game.question()
   def on_validate(w: Window):
      if not game.answer(w.answer.get()):
         w.show_error(game.expected_answer)
   def on_continue(w: Window):
      if not game:
         w.show_result(game.success, game.tries)
         return
      word, form = game.question()
      w.set_label(word, form)
   window = Window( word, form , on_validate=on_validate,
                    on_continue=on_continue)
   window.start()
