from abc import ABC, abstractmethod
from pippi import dsp
import random

from pippi.oscs import Osc


class Mutable(ABC):

    def __init__(self):
        self._sound = None

    @abstractmethod
    def mutate(self):
        pass

    def sound(self):
        return self._sound


class Kick(Mutable):

    def __init__(self, position, position_kernel=(-1, 1)):
        super().__init__()
        self.position = position
        self.position_kernel = position_kernel
        self._sound = dsp.read("samples/kick.wav")

    def mutate(self):
        new_kick = Kick(position=self.position,
                        position_kernel=self.position_kernel)

        new_kick.position += random.uniform(new_kick.position_kernel[0], new_kick.position_kernel[1])
        return new_kick


class Snare(Mutable):

    def __init__(self, position, position_kernel=(-0.5, 0.5)):
        super().__init__()
        self.position = position
        self.position_kernel = position_kernel
        self._sound = dsp.read("samples/snare.wav")

    def mutate(self):
        new_snare = Snare(position=self.position,
                          position_kernel=self.position_kernel)

        new_snare.position += random.uniform(new_snare.position_kernel[0], new_snare.position_kernel[1])
        return new_snare


class Hihat(Mutable):

    def __init__(self, position, position_kernel=(-0.1, 0.1)):
        super().__init__()
        self.position = position
        self.position_kernel = position_kernel
        self._sound = dsp.read("samples/hihat.wav")

    def mutate(self):
        new_hihat = Hihat(position=self.position,
                          position_kernel=self.position_kernel)

        new_hihat.position += random.uniform(new_hihat.position_kernel[0], new_hihat.position_kernel[1])
        return new_hihat


class Tone(Mutable):

    def __init__(self, position, frequency, position_kernel=(-0.1, 0.1), frequency_kernel=(-100, 100)):
        super().__init__()
        self.position = position
        self.frequency = frequency
        self.position_kernel = position_kernel
        self.frequency_kernel = frequency_kernel
        self._sound = dsp.read("samples/hihat.wav")

    def mutate(self):
        new_tone = Tone(position=self.position,
                        frequency=self.frequency,
                        position_kernel=self.position_kernel,
                        frequency_kernel=(-100, 100))

        new_tone.position += random.uniform(self.position_kernel[0], self.position_kernel[1])
        new_tone.frequency += random.uniform(self.frequency_kernel[0], self.frequency_kernel[1])
        return new_tone

    def sound(self):
        osc = Osc(dsp.SINE, freq=self.frequency)
        return osc.play(0.5)
