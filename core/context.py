import pygame


class PygameContext:
    def __init__(self, modules: list | None=None):
        self._modules = modules

    def __enter__(self):
        if self._modules:
            for module in self._modules:
                module.init()
            return
        
        pygame.init()

    def __exit__(self, exc_type, exc, tb):
        pygame.quit()
        return False