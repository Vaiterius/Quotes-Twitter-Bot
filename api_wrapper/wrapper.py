import requests


class MontyPythonAPI:
    """Wrapper for the Monty Python's Flying Circus API """
    
    def __init__(self):
        self.url = f"https://monty-pythons-flying-api.fly.dev/v1/"
    
    def _format(self, endpoint: str, params: dict):
        """Clean and validate data before requesting"""
        try:  # Check for parameters.
            arguments = ""
            if params:
                arguments += "?"
                for param, val in params.items():
                    arguments += f"{param}={val}&"
                arguments = arguments[:-1]
            response = requests.get(self.url + endpoint + arguments)
            
            return response.json()
        except requests.exceptions.ConnectionError as e:  # App is not on.
            return e
        except Exception as e:  # Something else happened.
            return e

    def get_actors(self):
        """Get a list of all the actors from the show"""
        return self._format("actors", None)

    def get_characters(self):
        """Get a list of all the characters from the show"""
        return self._format("characters", None)

    def get_random_quote(self, **kwargs):
        """Get a random quote.
        Kwargs: actor=None, episode=None, sketch=None,
                min_length=None, max_length=None
        """
        return self._format("quotes/random", kwargs)

    def get_random_episode(self, **kwargs):
        """Get a random episode.
        Kwargs: detailed=False
        """
        return self._format("episodes/random", kwargs)
    
    def get_episode(self, episode: int, **kwargs):
        """Get an episode by number.
        Args: episode
        Kwargs: detailed=False
        """
        return self._format(f"episodes/{episode}", kwargs)

    def get_sketches(self, **kwargs):
        """Get all sketches from the show.
        Kwargs: nested=False
        """
        return self._format("sketches", kwargs)

    def get_random_sketch(self, **kwargs):
        """Get a random sketch.
        Kwargs: detailed=False
        """
        return self._format("sketches/random", kwargs)
    
    def get_sketch_by_season(self, season: int, **kwargs):
        """Get all sketches from a particular season.
        Args: season
        Kwargs: nested=False
        """
        return self._format(f"sketches/season/{season}", kwargs)
    
    def get_sketch_by_episode(self, episode: int):
        """Get all sketches from a particular episode.
        Args: episode
        """
        return self._format(f"sketches/episode/{episode}", None)
    
    def get_sketch(self, sketch: str, **kwargs):
        """Get a particular sketch from the show.
        Args: sketch
        Kwargs: detailed=False
        """
        return self._format(f"sketches/sketch/{sketch}", kwargs)

