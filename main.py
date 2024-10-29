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

        # Load the Paris 2024 Olympics logo model
        logo_meshes = load_obj_file('models/logo-jo2024.obj')

        # Create a transformation matrix with 90-degree rotation and y-translation
        rotation_matrix = rotationMatrixX(np.radians(90))  # Rotate 90 degrees around X-axis
        translation_matrix = translationMatrix([0, 45, 0])  # Move to y=45
        # Combine rotation and translation into one matrix
        transformation_matrix = np.matmul(translation_matrix, rotation_matrix)
        self.paris_logo = DrawModelFromMesh(
            scene=self,
            M=transformation_matrix,  # Adjust the position and scale as needed
            mesh=logo_meshes[0],  # Use the first mesh from the OBJ file
            shader=TextureShader()  # Or use TextureShader() if the logo has textures
        )

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

            self.add_model(self.paris_logo)

          


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
        
        elif event.key == pygame.K_s:
            self.is_animating = True  # Start animation
            print('--> Start animation')
        elif event.key == pygame.K_f:
            self.is_animating = False  # Stop animation


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
