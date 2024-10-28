import pygame

# import the scene class
from scene import Scene

from lightSource import LightSource

from blender import load_obj_file

from BaseModel import DrawModelFromMesh

from shaders import *


class ParisScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        
        self.light = LightSource(self, position=[5., 3., 5.])

        # Load the Eiffel Tower model
        eiffel_meshes = load_obj_file('models/eiffel_tower.obj')
        # Check if the model has been loaded correctly
        if len(eiffel_meshes) == 0:
            print("Error: Eiffel Tower model could not be loaded. Check the file path and format.")
        else:
            # Adjust the scale and position as necessary
            self.eiffel_tower = DrawModelFromMesh(
                scene=self,
                M=poseMatrix(position=[0, 0, 0], scale=[0.1, 0.1, 0.1]),  # Adjust scale as needed
                mesh=eiffel_meshes[0],  # Assuming only one mesh
                shader=TextureShader()
            )

            # Add the Eiffel Tower to the scene
            self.add_model(self.eiffel_tower)


    def keyboard(self, event):
        '''
        Process additional keyboard events.
        '''
        super().keyboard(event)

        if event.key == pygame.K_1:
            print('--> using Flat shading')
            self.eiffel_tower.bind_shader(FlatShader())

        elif event.key == pygame.K_2:
            print('--> using Texture shading')
            self.eiffel_tower.bind_shader(TextureShader())


    def draw(self):
        '''
        Draw all models in the scene.
        '''
        # Clear the scene and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.camera.update()

        # Draw all models in the scene
        for model in self.models:
            model.draw()

        # Display the scene
        pygame.display.flip()


if __name__ == '__main__':
    # initialises the scene object
    # scene = Scene(shaders='gouraud')
    scene = ParisScene()

    # starts drawing the scene
    scene.run()
