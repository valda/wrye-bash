# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2014 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================

#--Game ESM/ESP/BSA files
#  These filenames need to be in lowercase,
bethDataFiles = set((
    #--Vanilla
    ur'fallout3.esm',
    ur'fallout - menuvoices.bsa',
    ur'fallout - meshes.bsa',
    ur'fallout - misc.bsa',
    ur'fallout - sound.bsa',
    ur'fallout - textures.bsa',
    ur'fallout - voices.bsa',
    #-- DLC
    ur'anchorage.esm',
    ur'anchorage - main.bsa',
    ur'anchorage - sounds.bsa',
    ur'thepitt.esm',
    ur'thepitt - main.bsa',
    ur'thepitt - sounds.bsa',
    ur'brokensteel.esm',
    ur'brokensteel - main.bsa',
    ur'brokensteel - sounds.bsa',
    ur'pointlookout.esm',
    ur'pointlookout - main.bsa',
    ur'pointlookout - sounds.bsa',
    ur'zeta.esm',
    ur'zeta - main.bsa',
    ur'zeta - sounds.bsa',
    ))

#--Every file in the Data directory from Bethsoft
allBethFiles = set((
    # Section 1: Vanilla files
    ur'Credits.txt',
    ur'CreditsWacky.txt',
    ur'Fallout3.esm',
    ur'Fallout - MenuVoices.bsa',
    ur'Fallout - Meshes.bsa',
    ur'Fallout - Misc.bsa',
    ur'Fallout - Sound.bsa',
    ur'Fallout - Textures.bsa',
    ur'Fallout - Voices.bsa',
    ur'LODSettings\aaaForgotten1.DLODSettings',
    ur'LODSettings\aaaForgotten4.DLODSettings',
    ur'LODSettings\aaaForgotten5.DLODSettings',
    ur'Music\Base\Base_01.mp3',
    ur'Music\Base\Base_02.mp3',
    ur'Music\Base\Base_03.mp3',
    ur'Music\Base\Base_04.mp3',
    ur'Music\Battle\Battle_01.mp3',
    ur'Music\Battle\Battle_02.mp3',
    ur'Music\Battle\Battle_03.mp3',
    ur'Music\Battle\Battle_04.mp3',
    ur'Music\Battle\Battle_05.mp3',
    ur'Music\Battle\Battle_06.mp3',
    ur'Music\Battle\Battle_07.mp3',
    ur'Music\Battle\Finale\Battle_01.mp3',
    ur'Music\Battle\Finale\Battle_02.mp3',
    ur'Music\Battle\Finale\Battle_03.mp3',
    ur'Music\Battle\Finale\Battle_04.mp3',
    ur'Music\Battle\Finale\Battle_05.mp3',
    ur'Music\Battle\Finale\Battle_06.mp3',
    ur'Music\Battle\Finale\Battle_07.mp3',
    ur'Music\Dungeon\Dungeon_01.mp3',
    ur'Music\Dungeon\Dungeon_02.mp3',
    ur'Music\Dungeon\Dungeon_03.mp3',
    ur'Music\Dungeon\Dungeon_04.mp3',
    ur'Music\Dungeon\Dungeon_05.mp3',
    ur'Music\Endgame\Endgame_01.mp3',
    ur'Music\Endgame\Endgame_02.mp3',
    ur'Music\Endgame\Endgame_03.mp3',
    ur'Music\Endgame\Endgame_04.mp3',
    ur'Music\Endgame\Endgame_05.mp3',
    ur'Music\Endgame\Endgame_06.mp3',
    ur'Music\Endgame\Endgame_07.mp3',
    ur'Music\Endgame\Endgame_08.mp3',
    ur'Music\Endgame\Endgame_09.mp3',
    ur'Music\Endgame\Endgame_11.mp3',
    ur'Music\Endgame\Endgame_12.mp3',
    ur'Music\Endgame\Endgame_14.mp3',
    ur'Music\Endgame\Endgame_15.mp3',
    ur'Music\Endgame\Endgame_17.mp3',
    ur'Music\Endgame\Endgame_18.mp3',
    ur'Music\Endgame\Endgame_19.mp3',
    ur'Music\Explore\Explore_01.mp3',
    ur'Music\Explore\Explore_02.mp3',
    ur'Music\Explore\Explore_03.mp3',
    ur'Music\Explore\Explore_04.mp3',
    ur'Music\Explore\Explore_05.mp3',
    ur'Music\Explore\Explore_06.mp3',
    ur'Music\Explore\Explore_07.mp3',
    ur'Music\Public\Public_01.mp3',
    ur'Music\Public\Public_02.mp3',
    ur'Music\Public\Public_03.mp3',
    ur'Music\Public\Public_04.mp3',
    ur'Music\Public\Public_05.mp3',
    ur'Music\Special\Death.mp3',
    ur'Music\Special\ExitTheVault.mp3',
    ur'Music\Special\MainTitle.mp3',
    ur'Music\Special\Success.mp3',
    ur'Music\Tension\Tension_01.mp3',
    ur'Music\TranquilityLane\MUS_TranquilityLane_01_LP.mp3',
    ur'Music\TranquilityLane\MUS_TranquilityLane_02_LP.mp3',
    ur'Shaders\shaderpackage002.sdp',
    ur'Shaders\shaderpackage003.sdp',
    ur'Shaders\shaderpackage004.sdp',
    ur'Shaders\shaderpackage006.sdp',
    ur'Shaders\shaderpackage007.sdp',
    ur'Shaders\shaderpackage009.sdp',
    ur'Shaders\shaderpackage010.sdp',
    ur'Shaders\shaderpackage011.sdp',
    ur'Shaders\shaderpackage012.sdp',
    ur'Shaders\shaderpackage013.sdp',
    ur'Shaders\shaderpackage014.sdp',
    ur'Shaders\shaderpackage015.sdp',
    ur'Shaders\shaderpackage016.sdp',
    ur'Shaders\shaderpackage017.sdp',
    ur'Shaders\shaderpackage018.sdp',
    ur'Shaders\shaderpackage019.sdp',
    ur'Video\1 year later.bik',
    ur'Video\2 weeks later.bik',
    ur'Video\3 years later.bik',
    ur'Video\6 years later.bik',
    ur'Video\9 years later.bik',
    ur'Video\B01.bik',
    ur'Video\B02.bik',
    ur'Video\B03.bik',
    ur'Video\B04.bik',
    ur'Video\B05.bik',
    ur'Video\B06.bik',
    ur'Video\B07.bik',
    ur'Video\B08.bik',
    ur'Video\B09.bik',
    ur'Video\B10.bik',
    ur'Video\B11.bik',
    ur'Video\B12.bik',
    ur'Video\B13.bik',
    ur'Video\B14.bik',
    ur'Video\B15.bik',
    ur'Video\B16.bik',
    ur'Video\B17.bik',
    ur'Video\B18.bik',
    ur'Video\B19.bik',
    ur'Video\B20.bik',
    ur'Video\B21.bik',
    ur'Video\B22.bik',
    ur'Video\B23.bik',
    ur'Video\B24.bik',
    ur'Video\B25.bik',
    ur'Video\B26.bik',
    ur'Video\B27.bik',
    ur'Video\B28.bik',
    ur'Video\B29.bik',
    ur'Video\Fallout INTRO Vsk.bik',
    # Section 2: DLCs
    ur'anchorage.esm',
    ur'anchorage - main.bsa',
    ur'anchorage - sounds.bsa',
    ur'thepitt.esm',
    ur'thepitt - main.bsa',
    ur'thepitt - sounds.bsa',
    ur'brokensteel.esm',
    ur'brokensteel - main.bsa',
    ur'brokensteel - sounds.bsa',
    ur'pointlookout.esm',
    ur'pointlookout - main.bsa',
    ur'pointlookout - sounds.bsa',
    ur'zeta.esm',
    ur'zeta - main.bsa',
    ur'zeta - sounds.bsa',
    ur'DLCList.txt',
    ))
