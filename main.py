import pygame
import numpy as np  # Ensure numpy is imported

# Import necessary classes and functions
from scene import Scene
from lightSource import LightSource
from blender import load_obj_file
from BaseModel import DrawModelFromMesh
from shaders import *
from matutils import rotationMatrixX, rotationMatrixY, translationMatrix, poseMatrix
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

class ParisScene(Scene):
    def __init__(self):
        super().__init__()
        
        self.light = LightSource(self, position=[5., 3., 5.])

        # Load the Paris 2024 Olympics logo model
        logo_meshes = load_obj_file('models/logo-jo2024.obj')

        # Initial transformation for the logo: Rotate 90 degrees around X-axis and move up to y=45
        self.logo_translation_matrix = translationMatrix([0, 45, 0])
        self.logo_initial_rotation = rotationMatrixX(np.radians(90))
        self.logo_transformation_matrix = np.matmul(self.logo_translation_matrix, self.logo_initial_rotation)

        # Variables for rotation animation
        self.logo_rotation_angle = 0  # Initial angle for rotation
        self.logo_rotation_active = False  # To track animation state
        
        # Create and position the logo model in the scene
        self.paris_logo = DrawModelFromMesh(
            scene=self,
            M=self.logo_transformation_matrix,
            mesh=logo_meshes[0],  # Use the first mesh from the OBJ file
            shader=TextureShader()  # Use TextureShader if the logo has textures
        )

        # Add the logo to the scene
        self.add_model(self.paris_logo)

        # Load the Eiffel Tower model
        eiffel_meshes = load_obj_file('models/eiffel_tower.obj')
        if len(eiffel_meshes) == 0:
            print("Error: Eiffel Tower model could not be loaded. Check the file path and format.")
        else:
            # Adjust the scale and position as necessary
            self.eiffel_tower = DrawModelFromMesh(
                scene=self,
                M=poseMatrix(position=[0, 0, 0], scale=[0.1, 0.1, 0.1]),
                mesh=eiffel_meshes[0],  # Assuming only one mesh
                shader=TextureShader()
            )
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
        
        elif event.key == pygame.K_s:
            self.logo_rotation_active = True  # Start animation
            print('--> Start animation')
        elif event.key == pygame.K_f:
            self.logo_rotation_active = False  # Stop animation
            print("Animation stopped.")

    def draw(self):
        '''
        Draw all models in the scene.
        '''
        # Clear the scene and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.camera.update()

        # If animation is active, update the rotation angle
        if self.logo_rotation_active:
            self.logo_rotation_angle += np.radians(1)  # Increment rotation by 2 degrees

            # Apply only Y-axis rotation for animation, maintaining the initial 90-degree tilt
            rotation_matrix = rotationMatrixY(self.logo_rotation_angle)
            self.paris_logo.M = np.matmul(self.logo_translation_matrix, 
                                          np.matmul(rotation_matrix, self.logo_initial_rotation))
        else:
            # Keep the logo in its initial transformation when not animating
            self.paris_logo.M = self.logo_transformation_matrix

        # Draw all models in the scene
        for model in self.models:
            model.draw()

        # Display the scene
        pygame.display.flip()

if __name__ == '__main__':
    # Initialize the scene object
    scene = ParisScene()

    # Start drawing the scene
    scene.run()
