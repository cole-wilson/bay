import bayan as b

ap = 20

cat = b.image('cb.jpeg')
dog = b.image('black-cat.png')

cat.pixelate(10)

cat.draw()


# compare = b.compare(cat,dog,ap,showprogress=True)

# cat.highlight(compare['ca'],ap)
# dog.highlight(compare['cb'],ap)