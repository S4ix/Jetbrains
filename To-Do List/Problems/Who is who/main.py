class Angel:
    color = "white"
    feature = "wings"
    home = "Heaven"


class Demon:
    color = "red"
    feature = "horns"
    home = "Hell"


satan = Demon()
lucifer = Angel()

print(f'{lucifer.color}\n{lucifer.feature}\n{lucifer.home}')
print(f'{satan.color}\n{satan.feature}\n{satan.home}')