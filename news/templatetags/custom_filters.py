from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   bad_words = ['Karina', 'chrmpionat']

   if not isinstance(value, str):
      raise TypeError(f"unresolved type '{type(value)}' expected  type 'str'")

   for word in value.split():
      if word.lower().strip(',') in bad_words:
         value = value.replace(word, f"{word[0]}{'*' * (len(word) - 1)}")
   """
   value: значение, к которому нужно применить фильтр
   """
   # Возвращаемое функцией значение подставится в шаблон.
   return value