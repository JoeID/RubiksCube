from ursina import *
import numpy as np
from ursina import curve
import random

app = Ursina()

player = Entity(model='cube', color=color.black, scale_y=1)
window.fullscreen=True


class Cube():
    def __init__(self):

        # self.repres contient 6 matrices qui contiennent les couleurs de chaque face, self.solutions contient les coups deja joues
        self.repres, self.solutions = [np.matrix([[c,c,c] for y in range(3)]) for c in ["blu", "gre", "ora", "red", "whi", "yel"]], []

        # ce sont les centres des faces, ils ne bougent pas
        c0, c1, c2, c3, c4, c5 = [Entity(model='cube', color=color.black, parent=player, position=e) for e in [(0,0,-1), (0,0,1), (-1,0,0), (1,0,0), (0,1,0), (0,-1,0)]]

        # ce sont six matrices contenant les objets 3d qui forment chaque face
        faceBlue = np.matrix([[c0 if x==y==0 else Entity(model='cube', color=color.black, parent=player, position=(x, y, -1)) for x in [-1,0,1]] for y in [1,0,-1]])
        faceGreen = np.matrix([[c1 if x==y==0 else Entity(model='cube', color=color.black, parent=player, position=(x, y, 1)) for x in [1,0,-1]] for y in [1,0,-1]])
        faceOrange = np.matrix([[faceGreen[0,2], Entity(model='cube', color=color.black, parent=player, position=(-1,1,0)), faceBlue[0,0]],
                                [faceGreen[1,2], c2, faceBlue[1,0]],
                                [faceGreen[2,2], Entity(model='cube', color=color.black, parent=player, position=(-1,-1,0)), faceBlue[2,0]]])
        faceRed = np.matrix([[faceBlue[0,2], Entity(model='cube', color=color.black, parent=player, position=(1,1,0)), faceGreen[0,0]],
                                [faceBlue[1,2], c3, faceGreen[1,0]],
                                [faceBlue[2,2], Entity(model='cube', color=color.black, parent=player, position=(1,-1,0)), faceGreen[2,0]]])
        faceWhite = np.matrix([[faceGreen[0,y] for y in range(2,-1,-1)],
                     [faceOrange[0,1], c4, faceRed[0,1]],
                     [faceBlue[0,y] for y in range(3)]])
        faceYellow = np.matrix([[faceBlue[2,y] for y in range(3)],
                     [faceOrange[2,1], c5, faceRed[2,1]],
                     [faceGreen[2,y] for y in range(2,-1,-1)]])

        self.cubef = [faceBlue, faceGreen, faceOrange, faceRed, faceWhite, faceYellow]
        self.centres = [c0, c1, c2, c3, c4, c5]

        #les cubes etant noirs, il faut ajouter les boutons colores
        for i in range(3):
            for j in range(3):
                Button(parent=faceBlue[i,j], position=(0,0,-0.51), rotation=(0,0,0), color=color.blue, disabled=True, scale=0.95)
        for i in range(3):
            for j in range(3):
                Button(parent=faceGreen[i,j], position=(0,0,0.51), rotation=(0,180,0), color=color.green, disabled=True, scale=0.95)
        for i in range(3):
            for j in range(3):
                Button(parent=faceOrange[i,j], position=(-0.51,0,0), rotation=(0,90,0), color=color.orange, disabled=True, scale=0.95)
        for i in range(3):
            for j in range(3):
                Button(parent=faceRed[i,j], position=(0.51,0,0), rotation=(0,-90,0), color=color.red, disabled=True, scale=0.95)
        for i in range(3):
            for j in range(3):
                if (i, j)==(1, 0): Button(parent=faceWhite[i,j], position=(0,0.51,0), rotation=(90,0,0), color=color.white, disabled=True, scale=0.95)
                elif (i, j)==(1,2): Button(parent=faceWhite[i,j], position=(0,0.51,0), rotation=(90,0,0), color=color.white, disabled=True, scale=0.95)
                else: Button(parent=faceWhite[i,j], position=(0,0.51,0), rotation=(90,0,0), color=color.white, disabled=True, scale=0.95)
        for i in range(3):
            for j in range(3):
                if (i, j)==(1, 0): Button(parent=faceYellow[i,j], position=(0,-0.51,0), rotation=(-90,0,0), color=color.yellow, disabled=True, scale=0.95)
                elif (i, j)==(1,2): Button(parent=faceYellow[i,j], position=(0,-0.51,0), rotation=(-90,0,0), color=color.yellow, disabled=True, scale=0.95)
                else: Button(parent=faceYellow[i,j], position=(0,-0.51,0), rotation=(-90,0,0), color=color.yellow, disabled=True, scale=0.95)

    def rotate(self, color):
        nums = {"blue": 0, "green": 1, "orange": 2, "red": 3, "white": 4, "yellow": 5}
        n = nums[color]
        for i in range(3):
            for j in range(3):
                if i!=1 or j!=1:
                    # on fait changer de parent chaque cube composant une face pour s'assurer que les cubes d'une face possedent pour parent le centre de cette face
                    self.cubef[n][i,j].reparent_to(self.centres[n])

        # on fait tourner le centre de la face selectionnee dans le sens trigo
        if n==0 or n==1:
            r = self.centres[n].rotation_z
            if n==0: self.centres[n].animate_rotation((0,0,r-90), duration=0.3, curve=curve.linear, interrupt=False)
            else: self.centres[n].animate_rotation((0,0,r+90), duration=0.3, curve=curve.linear, interrupt=False)
        elif n==2 or n==3:
            r = self.centres[n].rotation_x
            if n==2: self.centres[n].animate_rotation((r+90,0,0), duration=0.3, curve=curve.linear, interrupt=False)
            else: self.centres[n].animate_rotation((r-90,0,0), duration=0.3, curve=curve.linear, interrupt=False)
        else:
            r = self.centres[n].rotation_y
            if n==5: self.centres[n].animate_rotation((0,r+90,0), duration=0.3, curve=curve.linear, interrupt=False)
            else: self.centres[n].animate_rotation((0,r-90,0), duration=0.3, curve=curve.linear, interrupt=False)

        # on met a jour la liste self.cubef qui contient les matrices d'objets 3D
        # Tout d'abord, on fait tourner la matrice representant la face qui tourne
        self.cubef[n] = np.rot90(self.cubef[n], 1)

        # Bon la c'est la partie chiante, on met a jour les matrices des faces adjacentes a celle qui a tournee, il faut faire un schema pour comprendre
        if n==0:

            left = [self.cubef[nums["orange"]][i,2] for i in range(3)]
            for i in range(3):
                self.cubef[nums["orange"]][i,2]=self.cubef[nums["white"]][2,2-i]
            for i in range(3):
                self.cubef[nums["white"]][2,i]=self.cubef[nums["red"]][i,0]
            for i in range(3):
                self.cubef[nums["red"]][i,0]=self.cubef[nums["yellow"]][0,2-i]
            for i in range(3):
                self.cubef[nums["yellow"]][0,i]=left[i]

        elif n==1:

            left = [self.cubef[nums["red"]][i,2] for i in range(3)]
            for i in range(3):
                self.cubef[nums["red"]][i,2]=self.cubef[nums["white"]][0,i]
            for i in range(3):
                self.cubef[nums["white"]][0,i]=self.cubef[nums["orange"]][2-i,0]
            for i in range(3):
                self.cubef[nums["orange"]][i,0]=self.cubef[nums["yellow"]][2,i]
            for i in range(3):
                self.cubef[nums["yellow"]][2,i]=left[2-i]

        elif n==2:

            left = [self.cubef[nums["green"]][i,2] for i in range(3)]
            for i in range(3):
                self.cubef[nums["green"]][i,2]=self.cubef[nums["white"]][2-i,0]
            for i in range(3):
                self.cubef[nums["white"]][i,0]=self.cubef[nums["blue"]][i,0]
            for i in range(3):
                self.cubef[nums["blue"]][i,0]=self.cubef[nums["yellow"]][i,0]
            for i in range(3):
                self.cubef[nums["yellow"]][i,0]=left[2-i]

        elif n==3:

            left = [self.cubef[nums["blue"]][i,2] for i in range(3)]
            for i in range(3):
                self.cubef[nums["blue"]][i,2]=self.cubef[nums["white"]][i,2]
            for i in range(3):
                self.cubef[nums["white"]][i,2]=self.cubef[nums["green"]][2-i,0]
            for i in range(3):
                self.cubef[nums["green"]][i,0]=self.cubef[nums["yellow"]][2-i,2]
            for i in range(3):
                self.cubef[nums["yellow"]][i,2]=left[i]

        elif n==4:

            left = [self.cubef[nums["orange"]][0,i] for i in range(3)]
            for i in range(3):
                self.cubef[nums["orange"]][0,i]=self.cubef[nums["green"]][0,i]
            for i in range(3):
                self.cubef[nums["green"]][0,i]=self.cubef[nums["red"]][0,i]
            for i in range(3):
                self.cubef[nums["red"]][0,i]=self.cubef[nums["blue"]][0,i]
            for i in range(3):
                self.cubef[nums["blue"]][0,i]=left[i]

        elif n==5:

            left = [self.cubef[nums["orange"]][2,i] for i in range(3)]
            for i in range(3):
                self.cubef[nums["orange"]][2,i]=self.cubef[nums["blue"]][2,i]
            for i in range(3):
                self.cubef[nums["blue"]][2,i]=self.cubef[nums["red"]][2,i]
            for i in range(3):
                self.cubef[nums["red"]][2,i]=self.cubef[nums["green"]][2,i]
            for i in range(3):
                self.cubef[nums["green"]][2,i]=left[i]

        # et on garde trace de la rotation qui vient d'etre effectuee
        self.solutions.append(color)

    def sort(self):
        mouvs = ["blue", "green", "orange", "red", "white", "yellow"]
        s = Sequence()
        # on selectionne 20 fois une face au hasard, que l'on fait tourner
        for i in range(20):
            color = mouvs[random.randint(0,5)]
            s.append(
                Func(self.rotate, color)
            )
            s.append(
                Func(self.rotate_repres, color)
            )
            s.append(0.4) # pour ne pas que l'animation suivante commence avant que celle-ci ne se termine
        s.start()

    def rotate_repres(self, color):
        nums = {"blue": 0, "green": 1, "orange": 2, "red": 3, "white": 4, "yellow": 5}
        n = nums[color]

        self.repres[n] = np.rot90(self.repres[n], 1)
        if n==0:
            repres_left = [self.repres[nums["orange"]][i, 2] for i in range(3)]
            for i in range(3):
                self.repres[nums["orange"]][i,2]=self.repres[nums["white"]][2,2-i]
            for i in range(3):
                self.repres[nums["white"]][2, i] = self.repres[nums["red"]][i, 0]
            for i in range(3):
                self.repres[nums["red"]][i, 0] = self.repres[nums["yellow"]][0, 2 - i]
            for i in range(3):
                self.repres[nums["yellow"]][0,i]=repres_left[i]

        elif n==1:
            repres_left = [self.repres[nums["red"]][i,2] for i in range(3)]
            for i in range(3):
                self.repres[nums["red"]][i, 2] = self.repres[nums["white"]][0, i]
            for i in range(3):
                self.repres[nums["white"]][0, i] = self.repres[nums["orange"]][2 - i, 0]
            for i in range(3):
                self.repres[nums["orange"]][i, 0] = self.repres[nums["yellow"]][2, i]
            for i in range(3):
                self.repres[nums["yellow"]][2, i] = repres_left[2 - i]

        elif n==2:
            repres_left = [self.repres[nums["green"]][i, 2] for i in range(3)]
            for i in range(3):
                self.repres[nums["green"]][i, 2] = self.repres[nums["white"]][2 - i, 0]
            for i in range(3):
                self.repres[nums["white"]][i, 0] = self.repres[nums["blue"]][i, 0]
            for i in range(3):
                self.repres[nums["blue"]][i, 0] = self.repres[nums["yellow"]][i, 0]
            for i in range(3):
                self.repres[nums["yellow"]][i, 0] = repres_left[2 - i]

        elif n==3:
            repres_left = [self.repres[nums["blue"]][i,2] for i in range(3)]
            for i in range(3):
                self.repres[nums["blue"]][i, 2] = self.repres[nums["white"]][i, 2]
            for i in range(3):
                self.repres[nums["white"]][i, 2] = self.repres[nums["green"]][2 - i, 0]
            for i in range(3):
                self.repres[nums["green"]][i, 0] = self.repres[nums["yellow"]][2 - i, 2]
            for i in range(3):
                self.repres[nums["yellow"]][i, 2] = repres_left[i]

        elif n==4:
            repres_left = [self.repres[nums["orange"]][0, i] for i in range(3)]
            for i in range(3):
                self.repres[nums["orange"]][0, i] = self.repres[nums["green"]][0, i]
            for i in range(3):
                self.repres[nums["green"]][0, i] = self.repres[nums["red"]][0, i]
            for i in range(3):
                self.repres[nums["red"]][0, i] = self.repres[nums["blue"]][0, i]
            for i in range(3):
                self.repres[nums["blue"]][0, i] = repres_left[i]

        elif n==5:
            repres_left = [self.repres[nums["orange"]][2,i] for i in range(3)]
            for i in range(3):
                self.repres[nums["orange"]][2, i] = self.repres[nums["blue"]][2, i]
            for i in range(3):
                self.repres[nums["blue"]][2, i] = self.repres[nums["red"]][2, i]
            for i in range(3):
                self.repres[nums["red"]][2, i] = self.repres[nums["green"]][2, i]
            for i in range(3):
                self.repres[nums["green"]][2, i] = repres_left[i]

    def solve(self):
        S = Sequence()
        for color in self.solutions[::-1]:  # on parcourt la liste des rotations effectuees a l'envers
            # comme il faut faire tourner la face dans le sens anti trigo pour annuler le coup, on la fait tourner 3x dans le sens trigo
            self.rotate_repres(color)
            self.rotate_repres(color)
            self.rotate_repres(color)
            S.append(Func(self.rotate, color))
            S.append(0.4)
            S.append(Func(self.rotate, color))
            S.append(0.4)
            S.append(Func(self.rotate, color))
            S.append(0.4)
            
        S.start()


rubiksCube = Cube()


def update():
    # player represente le parent de tous les objets, cad le cube en entier
    player.rotation = (mouse.y*400, mouse.x*(-400))


def input(key):
    # b permet de faire tourner la face bleue, g verte, r rouge....
    if key=="b":
        rubiksCube.rotate("blue")
        rubiksCube.rotate_repres("blue")
    if key=="g":
        rubiksCube.rotate("green")
        rubiksCube.rotate_repres("green")
    if key=="o":
        rubiksCube.rotate("orange")
        rubiksCube.rotate_repres("orange")
    if key=="r":
        rubiksCube.rotate("red")
        rubiksCube.rotate_repres("red")
    if key=="w":
        rubiksCube.rotate("white")
        rubiksCube.rotate_repres("white")
    if key=="y":
        rubiksCube.rotate("yellow")
        rubiksCube.rotate_repres("yellow")
    if key=="s": # s permet de melanger le cube
        rubiksCube.sort()
    if key=="enter": # un appui sur la touche entree permet de *hem* resoudre le rubik's cube
        rubiksCube.solve()

#l'arriere plan
bg = Entity(parent=scene, model='quad', scale=(160, 90), z=2, color=color.light_gray)

app.run()
