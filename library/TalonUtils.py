from phoenix6.base_status_signal import BaseStatusSignal
from phoenix6.orchestra import Orchestra
from phoenix6.status_signal import StatusSignal
from phoenix6.configs import AudioConfigs
from phoenix6.hardware import TalonFX
from wpilib import DriverStation

class TalonUtils:
    orchestra:Orchestra
    talons:list[TalonFX]
    talonSignals:list[BaseStatusSignal]

    fileLoaded:bool = False

    @staticmethod
    def addMotor(talon:TalonFX) -> None:
        '''
        Adds motor to the processing list.
        - `talon` The motor to add.
        '''
        TalonUtils.talons.append(talon)
    
    @staticmethod
    def addSignal(signal:StatusSignal) -> None:
        TalonUtils.talonSignals.append(signal)
    
    @staticmethod
    def refreshAll() -> None:
        BaseStatusSignal.refresh_all(TalonUtils.talonSignals)
    
    @staticmethod
    def configureOrchestra(fileName:str) -> bool:
        '''
        Configure all motors to play a selected Chirp (CHRP) file in the deploy directory. Should be
        called once after addition of all Talons to TalonUtils.

        Use `loadOrchestraFile()` after configuration to change the played file.

        - `fileName` The path of the file to play.
        - `RETURNS` Whether loading the file was successful.

        '''
        audioCfg:AudioConfigs = AudioConfigs().with_allow_music_dur_disable(True)
        for talon in TalonUtils.talons:
            talon.configurator.apply(audioCfg)
            TalonUtils.orchestra.add_instrument(talon)
        return TalonUtils.loadOrchestraFile(fileName)
    
    @staticmethod
    def loadOrchestraFile(fileName:str) -> bool:
        '''
        Load the selected CHRP file located in the deployed directory.
        - `fileName` The name of the file to play.
        - `RETURNS` Whether loading the file was successful.
        '''
        TalonUtils.fileLoaded = TalonUtils.orchestra.load_music(fileName).is_ok()
        if not(TalonUtils.fileLoaded):
            TalonUtils.fileNotFound()
        return TalonUtils.fileLoaded

    @staticmethod
    def play() -> bool:
        '''
        Begin playback of the loaded file.
        - `RETURNS` Whether the operation was successful.
        '''
        if TalonUtils.fileLoaded:
            return TalonUtils.orchestra.play().is_ok()
        TalonUtils.fileNotFound()
        return False
    
    @staticmethod
    def stop() -> bool:
        '''
        Stop and restart playback of the loaded file.
        - `RETURNS` Whether the operation was successful.
        '''
        if TalonUtils.fileLoaded:
            return TalonUtils.orchestra.stop().is_ok()
        TalonUtils.fileNotFound()
        return False
    
    @staticmethod
    def pause() -> bool:
        '''
        Pause playback of the loaded file.
        - `RETURNS` Whether the operation was successful.
        '''
        if TalonUtils.fileLoaded:
            return TalonUtils.orchestra.pause().is_ok()
        TalonUtils.fileNotFound()
        return False
    
    @staticmethod
    def fileNotFound() -> None:
        TalonUtils.fileLoaded = False
        # TODO DriverStation.reportError doesn't seem to exist?
        print("CHRP file not loaded. Check that it is in the deploy directory & includes file extension.")