import rosenbot.elements as elements
import numpy as np
from pippi import dsp
import random


class Song:
    """
    Args:
        elements (List): A collection of (Mutable) elements
        score_function (Callable[float]): Callable function to calculate score
        initial_score (float): Initial score
        duration (int): Song duration in seconds

    """

    def __init__(self, elements, score_function, initial_score=0.0, duration=8, output=None):
        self._elements = elements
        self._initial_score = initial_score
        self._score = initial_score
        self._score_function = score_function
        self._duration = duration
        self._output = output

    def _make_step(self, elements):
        out = dsp.buffer(channels=2, frames=np.zeros((self._duration * 44100, 2)))
        for element in elements:
            out.dub(element.sound(), element.position)
        return out

    def mutate(self):
        new_elements = [element.mutate() for element in elements]
        out = self._make_step(new_elements)
        if self._output:
            out.write("{}/output-{}.wav".format(self._output, i))
        new_score = self._score_function()
        if new_score > self._score:
            self._elements = new_elements
            self._score = new_score
            print("Accepted mutation with score {}".format(new_score))
        else:
            print("Rejected mutation with score {}".format(new_score))

    def reset_score(self):
        self._score = self._initial_score


if __name__ == '__main__':

    # basic 8 second (2 measures, 60bpm) beat (kick, snare, hihat) with basic positional mutation

    kicks = [elements.Kick(position=t) for t in range(0, 8)]
    snares = [elements.Snare(position=t + 0.5) for t in range(0, 8)]
    hihats = [elements.Hihat(position=float(t) / 2.0) for t in range(0, 16)]
    tones = [elements.Tone(position=float(t) / 2.0, frequency=random.uniform(400, 2000)) for t in range(0, 16)]

    elements = []

    elements.extend(kicks)
    elements.extend(snares)
    elements.extend(hihats)
    elements.extend(tones)

    song = Song(elements=elements,
                initial_score=0,
                score_function=lambda: random.uniform(0, 10))

    ITERATIONS = 20

    for i in range(ITERATIONS):
        song.mutate()
        # reset the cost every 10 iterations
        if i % 10 == 0:
            song.reset_score()
