import cv2
import pygame
import os
import keyboard

script_dir = os.path.dirname(os.path.abspath(__file__))

video_mapping = {
    'a': os.path.join(script_dir, 'src/video1.mp4'),
    'b': os.path.join(script_dir, 'src/video2.mp4'),
    'c': os.path.join(script_dir, 'src/video3.mp4'),
}

class FullScreenApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        self.running = True
        self.clock = pygame.time.Clock()

        # Attacher les événements de touches
        keyboard.on_press(self.on_key_event)

        # Afficher l'image statique
        self.static_image = pygame.image.load(os.path.join(script_dir, 'src/static_image.jpg'))
        self.static_image = pygame.transform.scale(self.static_image, (self.screen_width, self.screen_height))
        self.display_static_image()

    def display_static_image(self):
        self.screen.blit(self.static_image, (0, 0))
        pygame.display.flip()

    def play_video(self, video_path):
        if os.path.exists(video_path):
            self.display_static_image()

            # Ouvrir la vidéo avec OpenCV
            self.cap = cv2.VideoCapture(video_path)

            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break

                # Convertir BGR à RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Redimensionner le frame à la taille de l'écran
                frame_resized = cv2.resize(frame_rgb, (self.screen_width, self.screen_height))

                # Convertir le frame en surface Pygame
                frame_surface = pygame.surfarray.make_surface(frame_resized.swapaxes(0, 1))

                # Afficher le frame
                self.screen.blit(frame_surface, (0, 0))
                pygame.display.flip()
                self.clock.tick(30)

            self.cap.release()
            self.display_static_image()
        else:
            print(f"Le fichier {video_path} n'existe pas.")

    def on_key_event(self, event):
        key = event.name
        if key in video_mapping:
            video_path = video_mapping[key]
            self.play_video(video_path)

def main():
    app = FullScreenApp()
    while app.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.running = False
        app.clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()