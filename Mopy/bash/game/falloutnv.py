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
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2011 Wrye Bash Team
#
# =============================================================================

"""This modules defines static data for use by bush, when
   Fallout: New Vegas is set at the active game."""

# Imports ----------------------------------------------------------------------
import struct
from .. import brec
from ..brec import *
from .. import bolt
from ..bolt import Flags, DataDict, StateError, _unicode, _encode
from .. import bush
from falloutnv_const import bethDataFiles, allBethFiles

# Util Constants ---------------------------------------------------------------
#--Null strings (for default empty byte arrays)
null1 = '\x00'
null2 = null1*2
null3 = null1*3
null4 = null1*4

#--Name of the game
displayName = u'Fallout New Vegas'
#--Name of the game as used in related filenames and paths.
fsName = u'FalloutNV'
#--Alternate display name of Wrye Bash when managing this game
altName = u'Wrye Flash NV'
#--Name of the default ini file.
defaultIniFile = u'Fallout_default.ini'

#--Exe to look for to see if this is the right game
exe = u'FalloutNV.exe'

#--Registry keys to read to find the install location
## These are relative to:
##  HKLM\Software
##  HKLM\Software\Wow6432Node
##  HKCU\Software
##  HKCU\Software\Wow6432Node
## Example: (u'Bethesda Softworks\\Oblivion',u'Installed Path')
regInstallKeys = [
    (u'Bethesda Softworks\\FalloutNV',u'Installed Path')
    ]

#--Patch information
## URL to download patches for the main game.
patchURL = u''
## Tooltip to display over the URL when displayed
patchTip = u''

#--URL to the Nexus site for this game
nexusUrl = u'http://www.nexusmods.com/newvegas/'
nexusName = u'New Vegas Nexus'
nexusKey = u'bash.installers.openNewVegasNexus'

#--Construction Set information
class cs:
    shortName = u'GECK'                  # Abbreviated name
    longName = u'Garden of Eden Creation Kit'                   # Full name
    exe = u'GECK.exe'                   # Executable to run
    seArgs = u'-editor'                     # Argument to pass to the SE to load the CS
    imageName = u'geck%s.png'                  # Image name template for the status bar

#--Script Extender information
class se:
    shortName = u'NVSE'                      # Abbreviated name
    longName = u'Fallout Script Extender'   # Full name
    exe = u'nvse_loader.exe'                 # Exe to run
    steamExe = u'nvse_loader.dll'           # Exe to run if a steam install
    url = u'http://nvse.silverlock.org/'     # URL to download from
    urlTip = u'http://nvse.silverlock.org/'  # Tooltip for mouse over the URL

#--Script Dragon
class sd:
    shortName = u''
    longName = u''
    installDir = u''

#--SkyProc Patchers
class sp:
    shortName = u''
    longName = u''
    installDir = u''

#--Quick shortcut for combining the SE and SD names
se_sd = u''

#--Graphics Extender information
class ge:
    shortName = u''
    longName = u''
    ## exe is treated specially here.  If it is a string, then it should
    ## be the path relative to the root directory of the game
    ## if it is list, each list element should be an iterable to pass to Path.join
    ## relative to the root directory of the game.  In this case, each filename
    ## will be tested in reverse order.  This was required for Oblivion, as the newer
    ## OBGE has a different filename than the older OBGE
    exe = u''
    url = u''
    urlTip = u''

#--4gb Launcher
class laa:
    name = u''           # Display name of the launcher
    exe = u'*DNE*'       # Executable to run
    launchesSE = False   # Whether the launcher will automatically launch the SE

# Files BAIN shouldn't skip
dontSkip = (
# Nothing so far
)

# Directories where specific file extensions should not be skipped by BAIN
dontSkipDirs = {
# Nothing so far
}

#--Folders BAIN should never CRC check in the Data directory
SkipBAINRefresh = set ((
    #Use lowercase names
    u'fnvedit backups',
))

#--Some stuff dealing with INI files
class ini:
    #--True means new lines are allowed to be added via INI tweaks
    #  (by default)
    allowNewLines = False

    #--INI Entry to enable BSA Redirection
    bsaRedirection = (u'Archive',u'sArchiveList')

#--Save Game format stuff
# Requires header.pcNick and header.playTime to be added to SaveHeader in bosh.py.
class ess:
    # Save file capabilities
    canReadBasic = True        # Can read the info needed for the Save Tab display
    canEditMasters = True      # Can adjust save file masters
    canEditMore = False         # Advanced editing

    # Save file extension.
    ext = u'.fos';

    @staticmethod
    def load(ins,header):
        """Extract basic info from save file.close
           At a minimum, this should set the following
           attrubutes in 'header':
            pcName
            pcLevel
            pcLocation
            gameDate
            gameDays
            gameTicks (seconds*1000)
            image (ssWidth,ssHeight,ssData)
            masters
        """
        if ins.read(11) != 'FO3SAVEGAME':
            raise Exception(u'Save file is not a Fallout New Vegas save game.')
        headerSize, = struct.unpack('I',ins.read(4))
        unknown,delim = struct.unpack('Ic',ins.read(5))
        header.language = ins.read(64)
        delim, = struct.unpack('c',ins.read(1))
        ssWidth,delim1,ssHeight,delim2,ssDepth,delim3 = struct.unpack('=IcIcIc',ins.read(15))
        #--Name, nickname, level, location, playtime
        size,delim = struct.unpack('Hc',ins.read(3))
        header.pcName = ins.read(size)
        delim, = struct.unpack('c',ins.read(1))
        size,delim = struct.unpack('Hc',ins.read(3))
        header.pcNick = ins.read(size)
        delim, = struct.unpack('c',ins.read(1))
        header.pcLevel,delim = struct.unpack('Ic',ins.read(5))
        size,delim = struct.unpack('Hc',ins.read(3))
        header.pcLocation = ins.read(size)
        delim, = struct.unpack('c',ins.read(1))
        size,delim = struct.unpack('Hc',ins.read(3))
        header.playTime = ins.read(size)
        delim, = struct.unpack('c',ins.read(1))
        #--Image Data
        ssData = ins.read(3*ssWidth*ssHeight)
        header.image = (ssWidth,ssHeight,ssData)
        #--Masters
        unknown,masterListSize = struct.unpack('=BI',ins.read(5))
        if unknown != 0x1B:
            raise Exception(u'%s: Unknown byte is not 0x1B.' % path)
        del header.masters[:]
        numMasters,delim = struct.unpack('Bc',ins.read(2))
        for count in range(numMasters):
            size,delim = struct.unpack('Hc',ins.read(3))
            header.masters.append(ins.read(size))
            delim, = struct.unpack('c',ins.read(1))


    @staticmethod
    def writeMasters(ins,out,header):
        """Rewrites masters of existing save file."""
        def unpack(format,size):
            return struct.unpack(format,ins.read(size))
        def pack(format,*args):
            out.write(struct.pack(format,*args))
        #--Header
        out.write(ins.read(11))
        #--SaveGameHeader
        size, = unpack('I',4)
        pack('I',size)
        out.write(ins.read(65))
        ssWidth,delim1,ssHeight,delim2 = unpack('=IcIc',10)
        pack('=IcIc',ssWidth,delim1,ssHeight,delim2)
        out.write(ins.read(size-80))
        #--Image Data
        out.write(ins.read(3*ssWidth*ssHeight))
        #--Skip old masters
        unknown,oldMasterListSize = unpack('=BI',5)
        if unknown != 0x1B:
            raise Exception(u'%s: Unknown byte is not 0x1B.' % path)
        numMasters,delim = unpack('Bc',2)
        oldMasters = []
        for count in range(numMasters):
            size,delim = unpack('Hc',3)
            oldMasters.append(ins.read(size))
            delim, = unpack('c',1)
        #--Write new masters
        newMasterListSize = 2 + (4 * len(header.masters))
        for master in header.masters:
            newMasterListSize += len(master)
        pack('=BI',unknown,newMasterListSize)
        pack('Bc',len(header.masters),'|')
        for master in header.masters:
            pack('Hc',len(master),'|')
            out.write(master.s)
            pack('c','|')
        #--Fids Address
        offset = out.tell() - ins.tell()
        fidsAddress, = unpack('I',4)
        pack('I',fidsAddress+offset)
        #--???? Address
        unknownAddress, = unpack('I',4)
        pack('I',unknownAddress+offset)
        #--???? Address
        unknownAddress, = unpack('I',4)
        pack('I',unknownAddress+offset)
        #--???? Address
        unknownAddress, = unpack('I',4)
        pack('I',unknownAddress+offset)
        #--???? Address
        unknownAddress, = unpack('I',4)
        pack('I',unknownAddress+offset)
        #--Copy remainder
        while True:
            buffer= ins.read(0x5000000)
            if not buffer: break
            out.write(buffer)
        return oldMasters

#--INI files that should show up in the INI Edits tab
iniFiles = [
    u'Fallout.ini',
    u'FalloutPrefs.ini',
    ]

#-- INI setting used to setup Save Profiles
## (section,key)
saveProfilesKey = (u'General',u'SLocalSavePath')

# Main master file, does not include Update.esm or DLC
mainGameMaster = u'FalloutNV.esm'
mainGameMasterLower = u'falloutnv.esm'

#--The main plugin Wrye Bash should look for
masterFiles = [
    u'FalloutNV.esm',
    ]

#--Plugin files that can't be deactivated
nonDeactivatableFiles = []

namesPatcherMaster = re.compile(ur"^FalloutNV.esm$",re.I|re.U)

#--The pickle file for this game.  Holds encoded GMST IDs from the big list below
pklfile = ur'bash\db\FalloutNV_ids.pkl'

#--Game ESM/ESP/BSA files
# bethDataFiles = set((
# Moved to falloutnv_const

#--Every file in the Data directory from Bethsoft
# allBethFiles = set((
# Moved to falloutnv_const

#--BAIN:
## These are the allowed default data directories that BAIN can install to
dataDirs = set((
    u'bash patches',
    u'distantlod',
    u'docs',
    u'facegen',
    u'fonts',
    u'menus',
    u'meshes',
    u'music',
    u'shaders',
    u'sound',
    u'textures',
    u'trees',
    u'video'
    ))
## These are additional special directories that BAIN can install to
dataDirsPlus = set((
    u'streamline',
    u'_tejon',
    u'ini tweaks',
    u'scripts',
    u'pluggy',
    u'ini',
    u'fose'))

# Installer -------------------------------------------------------------------
# ensure all path strings are prefixed with 'r' to avoid interpretation of
# accidental escape sequences
wryeBashDataFiles = set((
    ur'Bashed Patch.esp',
    ur'Bashed Patch, 0.esp',
    ur'Bashed Patch, 1.esp',
    ur'Bashed Patch, 2.esp',
    ur'Bashed Patch, 3.esp',
    ur'Bashed Patch, 4.esp',
    ur'Bashed Patch, 5.esp',
    ur'Bashed Patch, 6.esp',
    ur'Bashed Patch, 7.esp',
    ur'Bashed Patch, 8.esp',
    ur'Bashed Patch, 9.esp',
    ur'Bashed Patch, CBash.esp',
    ur'Bashed Patch, Python.esp',
    ur'Bashed Patch, FCOM.esp',
    ur'Bashed Patch, Warrior.esp',
    ur'Bashed Patch, Thief.esp',
    ur'Bashed Patch, Mage.esp',
    ur'Bashed Patch, Test.esp',
    ur'ArchiveInvalidationInvalidated!.bsa'
    ur'Fallout - AI!.bsa'
    ))
wryeBashDataDirs = set((
    ur'Bash Patches',
    ur'INI Tweaks'
    ))
ignoreDataFiles = set((
#    ur'NVSE\Plugins\Construction Set Extender.dll',
#    ur'NVSE\Plugins\Construction Set Extender.ini'
    ))
ignoreDataFilePrefixes = set(())
ignoreDataDirs = set((
#    ur'NVSE\Plugins\ComponentDLLs\CSE',
    ur'LSData'
    ))

# Function Info ---------------------------------------------------------------
conditionFunctionData = ( #--0: no param; 1: int param; 2: formid param
    (  1, 'GetDistance', 2, 0),
    (  5, 'GetLocked', 0, 0),
    (  6, 'GetPos', 1, 0),
    (  8, 'GetAngle', 1, 0),
    ( 10, 'GetStartingPos', 1, 0),
    ( 11, 'GetStartingAngle', 1, 0),
    ( 12, 'GetSecondsPassed', 0, 0),
    ( 14, 'GetActorValue', 1, 0),
    ( 18, 'GetCurrentTime', 0, 0),
    ( 24, 'GetScale', 0, 0),
    ( 25, 'IsMoving', 0, 0),
    ( 26, 'IsTurning', 0, 0),
    ( 27, 'GetLineOfSight', 2, 0),
    ( 32, 'GetInSameCell', 2, 0),
    ( 35, 'GetDisabled', 0, 0),
    ( 36, 'MenuMode', 1, 0),
    ( 39, 'GetDisease', 0, 0),
    ( 40, 'GetVampire', 0, 0),
    ( 41, 'GetClothingValue', 0, 0),
    ( 42, 'SameFaction', 2, 0),
    ( 43, 'SameRace', 2, 0),
    ( 44, 'SameSex', 2, 0),
    ( 45, 'GetDetected', 2, 0),
    ( 46, 'GetDead', 0, 0),
    ( 47, 'GetItemCount', 2, 0),
    ( 48, 'GetGold', 0, 0),
    ( 49, 'GetSleeping', 0, 0),
    ( 50, 'GetTalkedToPC', 0, 0),
    ( 53, 'GetScriptVariable', 2, 1),
    ( 56, 'GetQuestRunning', 2, 0),
    ( 58, 'GetStage', 2, 0),
    ( 59, 'GetStageDone', 2, 1),
    ( 60, 'GetFactionRankDifference', 2, 2),
    ( 61, 'GetAlarmed', 0, 0),
    ( 62, 'IsRaining', 0, 0),
    ( 63, 'GetAttacked', 0, 0),
    ( 64, 'GetIsCreature', 0, 0),
    ( 65, 'GetLockLevel', 0, 0),
    ( 66, 'GetShouldAttack', 2, 0),
    ( 67, 'GetInCell', 2, 0),
    ( 68, 'GetIsClass', 2, 0),
    ( 69, 'GetIsRace', 2, 0),
    ( 70, 'GetIsSex', 1, 0),
    ( 71, 'GetInFaction', 2, 0),
    ( 72, 'GetIsID', 2, 0),
    ( 73, 'GetFactionRank', 2, 0),
    ( 74, 'GetGlobalValue', 2, 0),
    ( 75, 'IsSnowing', 0, 0),
    ( 76, 'GetDisposition', 2, 0),
    ( 77, 'GetRandomPercent', 0, 0),
    ( 79, 'GetQuestVariable', 2, 1),
    ( 80, 'GetLevel', 0, 0),
    ( 81, 'GetArmorRating', 0, 0),
    ( 84, 'GetDeadCount', 2, 0),
    ( 91, 'GetIsAlerted', 0, 0),
    ( 98, 'GetPlayerControlsDisabled', 0, 0),
    ( 99, 'GetHeadingAngle', 2, 0),
    (101, 'IsWeaponOut', 0, 0),
    (102, 'IsTorchOut', 0, 0),
    (103, 'IsShieldOut', 0, 0),
    (106, 'IsFacingUp', 0, 0),
    (107, 'GetKnockedState', 0, 0),
    (108, 'GetWeaponAnimType', 0, 0),
    (109, 'IsWeaponSkillType', 1, 0),
    (110, 'GetCurrentAIPackage', 0, 0),
    (111, 'IsWaiting', 0, 0),
    (112, 'IsIdlePlaying', 0, 0),
    (116, 'GetMinorCrimeCount', 0, 0),
    (117, 'GetMajorCrimeCount', 0, 0),
    (118, 'GetActorAggroRadiusViolated', 0, 0),
    (122, 'GetCrime', 2, 1),
    (123, 'IsGreetingPlayer', 0, 0),
    (125, 'IsGuard', 0, 0),
    (127, 'HasBeenEatan', 0, 0),
    (128, 'GetFatiguePercentage', 0, 0),
    (129, 'GetPCIsClass', 2, 0),
    (130, 'GetPCIsRace', 2, 0),
    (131, 'GetPCIsSex', 1, 0),
    (132, 'GetPCInFaction', 2, 0),
    (133, 'SameFactionAsPC', 0, 0),
    (134, 'SameRaceAsPC', 0, 0),
    (135, 'SameSexAsPC', 0, 0),
    (136, 'GetIsReference', 2, 0),
    (141, 'IsTalking', 0, 0),
    (142, 'GetWalkSpeed', 0, 0),
    (143, 'GetCurrentAIProcedure', 0, 0),
    (144, 'GetTrespassWarningLevel', 0, 0),
    (145, 'IsTrespassing', 0, 0),
    (146, 'IsInMyOwnedCell', 0, 0),
    (147, 'GetWindSpeed', 0, 0),
    (148, 'GetCurrentWeatherPercent', 0, 0),
    (149, 'GetIsCurrentWeather', 2, 0),
    (150, 'IsContinuingPackagePCNear', 0, 0),
    (153, 'CanHaveFlames', 0, 0),
    (154, 'HasFlames', 0, 0),
    (157, 'GetOpenState', 0, 0),
    (159, 'GetSitting', 0, 0),
    (160, 'GetFurnitureMarkerID', 0, 0),
    (161, 'GetIsCurrentPackage', 2, 0),
    (162, 'IsCurrentFurnitureRef', 2, 0),
    (163, 'IsCurrentFurnitureObj', 2, 0),
    (170, 'GetDayOfWeek', 0, 0),
    (172, 'GetTalkedToPCParam', 2, 0),
    (175, 'IsPCSleeping', 0, 0),
    (176, 'IsPCAMurderer', 0, 0),
    (180, 'GetDetectionLevel', 2, 0),
    (182, 'GetEquipped', 2, 0),
    (185, 'IsSwimming', 0, 0),
    (190, 'GetAmountSoldStolen', 0, 0),
    (192, 'GetIgnoreCrime', 0, 0),
    (193, 'GetPCExpelled', 2, 0),
    (195, 'GetPCFactionMurder', 2, 0),
    (197, 'GetPCEnemyofFaction', 2, 0),
    (199, 'GetPCFactionAttack', 2, 0),
    (203, 'GetDestroyed', 0, 0),
    (214, 'HasMagicEffect', 2, 0),
    (215, 'GetDefaultOpen', 0, 0),
    (219, 'GetAnimAction', 0, 0),
    (223, 'IsSpellTarget', 2, 0),
    (224, 'GetVATSMode', 0, 0),
    (225, 'GetPersuasionNumber', 0, 0),
    (226, 'GetSandman', 0, 0),
    (227, 'HasCannibal', 0, 0),
    (228, 'GetIsClassDefault', 2, 0),
    (229, 'GetClassDefaultMatch', 0, 0),
    (230, 'GetInCellParam', 2, 2),
    (235, 'GetVatsTargetHeight', 0, 0),
    (237, 'GetIsGhost', 0, 0),
    (242, 'GetUnconscious', 0, 0),
    (244, 'GetRestrained', 0, 0),
    (246, 'GetIsUsedItem', 2, 0),
    (247, 'GetIsUsedItemType', 1, 0),
    (254, 'GetIsPlayableRace', 0, 0),
    (255, 'GetOffersServicesNow', 0, 0),
    (258, 'GetUsedItemLevel', 0, 0),
    (259, 'GetUsedItemActivate', 0, 0),
    (264, 'GetBarterGold', 0, 0),
    (265, 'IsTimePassing', 0, 0),
    (266, 'IsPleasant', 0, 0),
    (267, 'IsCloudy', 0, 0),
    (274, 'GetArmorRatingUpperBody', 0, 0),
    (277, 'GetBaseActorValue', 1, 0),
    (278, 'IsOwner', 2, 0),
    (280, 'IsCellOwner', 2, 2),
    (282, 'IsHorseStolen', 0, 0),
    (285, 'IsLeftUp', 0, 0),
    (286, 'IsSneaking', 0, 0),
    (287, 'IsRunning', 0, 0),
    (288, 'GetFriendHit', 2, 0),
    (289, 'IsInCombat', 0, 0),
    (300, 'IsInInterior', 0, 0),
    (304, 'IsWaterObject', 0, 0),
    (306, 'IsActorUsingATorch', 0, 0),
    (309, 'IsXBox', 0, 0),
    (310, 'GetInWorldspace', 2, 0),
    (312, 'GetPCMiscStat', 1, 0),
    (313, 'IsActorEvil', 0, 0),
    (314, 'IsActorAVictim', 0, 0),
    (315, 'GetTotalPersuasionNumber', 0, 0),
    (318, 'GetIdleDoneOnce', 0, 0),
    (320, 'GetNoRumors', 0, 0),
    (323, 'WhichServiceMenu', 0, 0),
    (327, 'IsRidingHorse', 0, 0),
    (332, 'IsInDangerousWater', 0, 0),
    (338, 'GetIgnoreFriendlyHits', 0, 0),
    (339, 'IsPlayersLastRiddenHorse', 0, 0),
    (353, 'IsActor', 0, 0),
    (354, 'IsEssential', 0, 0),
    (358, 'IsPlayerMovingIntoNewSpace', 0, 0),
    (361, 'GetTimeDead', 0, 0),
    (362, 'GetPlayerHasLastRiddenHorse', 0, 0),
    (365, 'IsChild', 0, 0),
    (367, 'GetLastPlayerAction', 0, 0),
    (368, 'IsPlayerActionActive', 1, 0),
    (370, 'IsTalkingActivatorActor', 2, 0),
    (372, 'IsInList', 2, 0),
    (382, 'GetHasNote', 2, 1),
    (391, 'GetHitLocation', 0, 0),
    (392, 'IsPC1stPerson', 0, 0),
    (397, 'GetCauseofDeath', 0, 0),
    (398, 'IsLimbGone', 1, 0),
    (399, 'IsWeaponInList', 2, 0),
    (403, 'HasFriendDisposition', 0, 0),
    (408, 'GetVATSValue', 1, 2),
    (409, 'IsKiller', 2, 0),
    (410, 'IsKillerObject', 2, 0),
    (411, 'GetFactionCombatReaction', 2, 2),
    (415, 'Exists', 2, 0),
    (416, 'GetGroupMemberCount', 0, 0),
    (417, 'GetGroupTargetCount', 0, 0),
    (420, 'GetObjectiveCompleted', 2, 1),
    (421, 'GetObjectiveDisplayed', 2, 1),
    (427, 'GetIsVoiceType', 2, 0),
    (428, 'GetPlantedExplosive', 0, 0),
    (430, 'IsActorTalkingThroughActivator', 0, 0),
    (431, 'GetHealthPercentage', 0, 0),
    (433, 'GetIsObjectType', 1, 0),
    (435, 'GetDialogueEmotion', 0, 0),
    (436, 'GetDialogueEmotionValue', 0, 0),
    (438, 'GetIsCreatureType', 1, 0),
    (446, 'GetInZone', 2, 1),
    (449, 'HasPerk', 2, 1),
    (450, 'GetFactionRelation', 1, 0),
    (451, 'IsLastIdlePlayed', 2, 0),
    (454, 'GetPlayerTeammate', 0, 0),
    (455, 'GetPlayerTeammateCount', 0, 0),
    (459, 'GetActorCrimePlayerEnemy', 0, 0),
    (460, 'GetActorFactionPlayerEnemy', 0, 0),
    (462, 'IsPlayerTagSkill', 1, 0),
    (464, 'IsPlayerGrabbedRef', 1, 0),
    (471, 'GetDestructionStage', 0, 0),
    (474, 'GetIsAlignment', 1, 0),
    (478, 'GetThreatRatio', 2, 0),
    (480, 'GetIsUsedItemEquipType', 1, 0),
    (489, 'GetConcussed', 0, 0),
    (492, 'GetMapMarkerVisible', 1, 1),
    (495, 'GetPermanentActorValue', 1, 0),
    (496, 'GetKillingBlowLimb', 0, 0),
    (500, 'GetWeaponHealthPerc', 0, 0),
    (503, 'GetRadiationLevel', 0, 0),
    (510, 'GetLastHitCritical', 0, 0),
    (515, 'IsCombatTarget', 2, 0),
    (518, 'GetVATSRightAreaFree', 1, 0),
    (519, 'GetVATSLeftAreaFree', 1, 0),
    (520, 'GetVATSBackAreaFree', 1, 0),
    (521, 'GetVATSFrontAreaFree', 1, 0),
    (522, 'GetIsLockBroken', 0, 0),
    (523, 'IsPS3', 0, 0),
    (524, 'IsWin32', 0, 0),
    (525, 'GetVATSRightTargetVisible', 1, 0),
    (526, 'GetVATSLeftTargetVisible', 1, 0),
    (527, 'GetVATSBackTargetVisible', 1, 0),
    (528, 'GetVATSFrontTargetVisible', 1, 0),
    (531, 'IsInCriticalStage', 1, 0),
    (533, 'GetXPForNextLevel', 0, 0),
    (546, 'GetQuestCompleted', 2, 0),
    (550, 'IsGoreDisabled', 0, 0),
    (555, 'GetSpellUsageNum', 2, 0),
    (557, 'GetActorsInHigh', 0, 0),
    (558, 'HasLoaded3D', 0, 0),
    (573, 'GetReputation', 2, 1),
    (574, 'GetReputationPct', 2, 1),
    (575, 'GetReputationThreshold', 2, 1),
    (586, 'IsHardcore', 0, 0),
    (601, 'GetForceHitReaction', 0, 0),
    (607, 'ChallengeLocked', 2, 0),
    (610, 'GetCasinoWinningStage', 2, 0),
    (612, 'PlayerInRegion', 2, 0),
    (614, 'GetChallengeCompleted', 2, 0),
    (619, 'IsAlwaysHardcore', 0, 0),

    # extended by NVSE
    (1024, 'GetNVSEVersion', 0, 0),
    (1025, 'GetNVSERevision', 0, 0),
    (1028, 'GetWeight', 2, 0),
    (1082, 'IsKeyPressed', 1, 0),
    (1165, 'GetWeaponHasScope', 0, 0),
    (1166, 'IsControlPressed', 1, 0),
    (1213, 'GetNVSEBeta', 0, 0),
    )
allConditions = set(entry[0] for entry in conditionFunctionData)
fid1Conditions = set(entry[0] for entry in conditionFunctionData if entry[2] == 2)
fid2Conditions = set(entry[0] for entry in conditionFunctionData if entry[3] == 2)

#--List of GMST's in the main plugin (FalloutNV.esm) that have 0x00000000
#  as the form id.  Any GMST as such needs it Editor Id listed here.
gmstEids = ['fPlayerDeathReloadTime','iMapMarkerVisibleDistance','fVanityModeWheelMax','fChase3rdPersonZUnitsPerSecond',
    'fAutoAimMaxDegreesMiss','iHoursToRespawnCell','fEssentialDeathTime','fJumpHeightMin','fPlayerPipBoyLightTimer',
    'iAINumberActorsComplexScene','iHackingMaxWords','fGunShellLifetime','fGunShellCameraDistance','fGunDecalCameraDistance',
    'iDebrisMaxCount','iHackingDumpRate','iHackingInputRate','iHackingOutputRate','iHackingFlashOffDuration',
    'iHackingFlashOnDuration','iComputersDisplayRateMenus','iComputersDisplayRateNotes','iInventoryAskQuantityAt',
    'iNumberActorsInCombatPlayer','iNumberActorsAllowedToFollowPlayer','iRemoveExcessDeadCount','iRemoveExcessDeadTotalActorCount',
    'iRemoveExcessDeadComplexTotalActorCount','iRemoveExcessDeadComplexCount', 'fRemoveExcessDeadTime','fRemoveExcessComplexDeadTime',
    'iLevItemLevelDifferenceMax','fMoveWeightMax',
    ]

#--GLOB record tweaks used by bosh's GmstTweaker
#  Each entry is a tuple in the following format:
#    (DisplayText, MouseoverText, GLOB EditorID, Option1, Option2, Option3, ..., OptionN)
#    -EditorID can be a plain string, or a tuple of multiple Editor IDs.  If it's a tuple,
#     then Value (below) must be a tuple of equal length, providing values for each GLOB
#  Each Option is a tuple:
#    (DisplayText, Value)
#    - If you enclose DisplayText in brackets like this: _(u'[Default]'), then the patcher
#      will treat this option as the default value.
#    - If you use _(u'Custom') as the entry, the patcher will bring up a number input dialog
#  To make a tweak Enabled by Default, enclose the tuple entry for the tweak in a list, and make
#  a dictionary as the second list item with {'defaultEnabled':True}.  See the UOP Vampire face
#  fix for an example of this (in the GMST Tweaks)
## NOTE: only required if the GmstTweaker has been enabled for this game
GlobalsTweaks = [
    (_(u'Timescale'),_(u'Timescale will be set to:'),
        u'timescale',
        (u'1',         1),
        (u'8',         8),
        (u'10',       10),
        (u'12',       12),
        (u'20',       20),
        (u'24',       24),
        (u'[30]',     30),
        (u'40',       40),
        (_(u'Custom'), 30),
        ),
    ]

#--GMST record tweaks used by bosh's GmstTweaker
#  Each entry is a tuple in the following format:
#    (DisplayText, MouseoverText, GMST EditorID, Option1, Option2, Option3, ..., OptionN)
#    -EditorID can be a plain string, or a tuple of multiple Editor IDs.  If it's a tuple,
#     then Value (below) must be a tuple of equal length, providing values for each GMST
#  Each Option is a tuple:
#    (DisplayText, Value)
#    - If you enclose DisplayText in brackets like this: _(u'[Default]'), then the patcher
#      will treat this option as the default value.
#    - If you use _(u'Custom') as the entry, the patcher will bring up a number input dialog
#  To make a tweak Enabled by Default, enclose the tuple entry for the tweak in a list, and make
#  a dictionary as the second list item with {'defaultEnabled':True}.  See the UOP Vampire face
#  fix for an example of this (in the GMST Tweaks)
## NOTE: only required if the GmstTweaker has been enabled for this game
GmstTweaks = [
    (_(u'Actor Strength Encumbrance Multiplier'),_(u"Actor's Strength X this = Actor's Encumbrance capacity."),
        (u'fActorStrengthEncumbranceMult',),
        (u'1',                 1.0),
        (u'3',                 3.0),
        (u'[5]',               5.0),
        (u'8',                 8.0),
        (u'10',               10.0),
        (u'20',               20.0),
        (_(u'Unlimited'), 999999.0),
        (_(u'Custom'),         5.0),
        ),
    (_(u'Camera: Chase Distance'),_(u"Distance camera can be moved away from PC using mouse wheel."),
        ('fVanityModeWheelMax', 'fChase3rdPersonZUnitsPerSecond'),
        (_('x 1.5'),600.0*1.5, 800.0*1.5),
        (_('x 2'),  600.0*2.0, 800.0*2),
        (_('x 3'),  600.0*3.0, 800.0*3),
        (_('x 5'),  600.0*5.0, 800.0*5),
        (_('x 10'), 600.0*10,  5000),
        (_(u'Custom'),600,      800),
        ),
    (_(u'Compass: POI Recognition'),_(u"Distance at which POI markers begin to show on compass."),
        ('iMapMarkerVisibleDistance',),
        (_('x 0.05'),1000),
        (_('x 0.25'),5000),
        (_('x 0.50'),10000),
        (_('x 0.75'),15000),
        (_(u'Custom (base 1200)'),1200),
        ),
    (_(u'Essential NPC Unconsciousness'),_(u"Time which essential NPCs stay unconscious."),
        ('fEssentialDeathTime',),
        (_(u'[10 Seconds]'),10.0),
        (_(u'20 Seconds'),20.0),
        (_(u'30 Seconds'),30.0),
        (_(u'1 Minute'),60.0),
        (_(u'1 1/2 Minutes'),1.5*60.0),
        (_(u'2 Minutes'),2*60.0),
        (_(u'3 Minutes'),3*60.0),
        (_(u'5 Minutes'),5*60.0),
        (_(u'Custom (in seconds)'),10),
        ),
    (_(u'Jump Higher'),_(u"Height player can jump to."),
        ('fJumpHeightMin',),
        (_('x 1.1'),64.0*1.1),
        (_('x 1.2'),64.0*1.2),
        (_('x 1.4'),64.0*1.4),
        (_('x 1.6'),64.0*1.6),
        (_('x 1.8'),64.0*1.8),
        (_('x 2.0'),64.0*2.0),
        (_('x 3.0'),64.0*3.0),
        (_(u'Custom'),64),
        ),
    (_(u'Camera: PC Death Time'),_(u"Time after player's death before reload menu appears."),
        ('fPlayerDeathReloadTime',),
        (_(u'15 Seconds'),15.0),
        (_(u'30 Seconds'),30.0),
        (_(u'1 Minute'),60.0),
        (_(u'5 Minute'),300.0),
        (_(u'Unlimited'),9999999.0),
        (_(u'Custom'),15),
        ),
    (_(u'Cell Respawn Time'),_(u"Time before unvisited cell respawns. But longer times increase save sizes."),
        ('iHoursToRespawnCell',),
        (_(u'1 Day'),24*1),
        (_(u'[3 Days]'),24*3),
        (_(u'5 Days'),24*5),
        (_(u'10 Days'),24*10),
        (_(u'20 Days'),24*20),
        (_(u'1 Month'),24*30),
        (_(u'6 Months'),24*182),
        (_(u'1 Year'),24*365),
        (_(u'Custom (in hours)'),72),
        ),
    (_(u'Cost Multiplier: Repair'),_(u"Cost factor for repairing items."),
        ('fItemRepairCostMult',),
        ('1.0',1.0),
        ('1.25',1.25),
        ('1.5',1.5),
        ('1.75',1.75),
        ('[2.0]',2.0),
        ('2.5',2.5),
        ('3.0',3.0),
        (_(u'Custom'),2.0),
        ),
    (_(u'Combat: Max Actors'),_(u"Maximum number of actors that can actively be in combat with the player."),
        ('iNumberActorsInCombatPlayer',),
        ('[10]',10),
        ('15',15),
        ('20',20),
        ('30',30),
        ('40',40),
        ('50',50),
        ('80',80),
        (_(u'Custom'),10),
        ),
    (_(u'AI: Max Active Actors'),_(u"Maximum actors whose AI can be active. Must be higher than Combat: Max Actors"),
        ('iAINumberActorsComplexScene',),
        ('20',20),
        ('[25]',25),
        ('30',30),
        ('35',35),
        (_(u'MMM Default: 40'),40),
        ('50',50),
        ('60',60),
        ('100',100),
        (_(u'Custom'),25),
        ),
    (_(u'Companions: Max Number'),_(u"Maximum number of actors following the player"),
        ('iNumberActorsAllowedToFollowPlayer',),
        ('2',2),
        ('4',4),
        ('[6]',6),
        ('8',8),
        ('10',10),
        (_(u'Custom'),6),
        ),
    (_(u'AI: Max Dead Actors'),_(u"Maximum number of dead actors allowed before they're removed."),
        ('iRemoveExcessDeadCount', 'iRemoveExcessDeadTotalActorCount','iRemoveExcessDeadComplexTotalActorCount',
         'iRemoveExcessDeadComplexCount', 'fRemoveExcessDeadTime','fRemoveExcessComplexDeadTime'),
        (_('[x 1]'),int(15*1)  , int(20*1)  , int(20*1)  , int(3*1), 10.0*1.0, 2.5*1.0),
        (_('x 1.5'),int(15*1.5), int(20*1.5), int(20*1.5), int(3*2), 10.0*3.0, 2.5*3.0),
        (_('x 2'),  int(15*2)  , int(20*2)  , int(20*2)  , int(3*3), 10.0*5.0, 2.5*5.0),
        (_('x 2.5'),int(15*2.5), int(20*2.5), int(20*2.5), int(3*4), 10.0*7.0, 2.5*7.0),
        (_('x 3'),  int(15*3)  , int(20*3)  , int(20*3)  , int(3*5), 10.0*9.0, 2.5*9.0),
        (_('x 3.5'),int(15*3.5), int(20*3.5), int(20*3.5), int(3*6), 10.0*11.0, 2.5*11.0),
        (_('x 4'),  int(15*4)  , int(20*4)  , int(20*4)  , int(3*7), 10.0*13.0, 2.5*13.0),
        (_(u'Custom'),15,20,20,3,10,2.5),
        ),
    (_(u'Inventory Quantity Prompt'),_(u"Number of items in a stack at which point Fallout prompts for a quantity."),
        ('iInventoryAskQuantityAt',),
        ('1',1),
        ('2',2),
        ('[3]',3),
        ('4',4),
        ('10',10),
        (_(u'No Prompt'),99999),
        (_(u'Custom'),3),
        ),
    (_(u'Gore: Combat Dismember Part Chance'),_(u"The chance that body parts will be dismembered."),
        ('iCombatDismemberPartChance',),
        ('0',0),
        ('25',25),
        ('[50]',50),
        ('80',80),
        ('100',100),
        (_(u'Custom'),50),
        ),
    (_(u'Gore: Combat Explode Part Chance'),_(u"The chance that body parts will be explode."),
        ('iCombatExplodePartChance',),
        ('0',0),
        ('25',25),
        ('50',50),
        ('[75]',75),
        ('100',100),
        (_(u'Custom'),75),
        ),
    (_(u'Leveled Item Max level difference'),_(u"Maximum difference to player level for leveled items."),
        ('iLevItemLevelDifferenceMax',),
        ('1',1),
        ('5',5),
        ('[8]',8),
        ('10',10),
        ('20',20),
        (_(u'Unlimited'),9999),
        (_(u'Custom'),8),
        ),
    (_(u'Movement Base Speed'),_(u"Base Movement speed."),
        ('fMoveBaseSpeed',),
        ('[77.0]',77.0),
        ('90.0',90.0),
        (_(u'Custom'),77.0),
        ),
    (_(u'Movement Sneak Multiplier'),_(u"Movement speed is multiplied by this when the actor is sneaking."),
        ('fMoveSneakMult',),
        ('[0.57]',0.57),
        ('0.66',0.66),
        (_(u'Custom'),0.57),
        ),
    (_(u'Combat: Player Damage Multiplier in VATS'),_(u"Multiplier of damage that player receives in VATS."),
        ('fVATSPlayerDamageMult',),
        (_('0.10'),0.1),
        (_('0.25'),0.25),
        (_('0.50'),0.5),
        (_('[0.75]'),0.75),
        (_('1.00'),1.0),
        (_(u'Custom'),0.75),
        ),
    (_(u'Combat: Auto Aim Fix'),_(u"Increase Auto Aim settings to a level at which Snipers can benefit from them."),
        ('fAutoAimMaxDistance', 'fAutoAimScreenPercentage', 'fAutoAimMaxDegrees', 'fAutoAimMissRatioLow', 'fAutoAimMissRatioHigh', 'fAutoAimMaxDegreesMiss'),
        (_(u'Harder'),50000.00, -180.00, 1.10, 1.00, 1.30, 3.00),
        ),
    (_(u'PipBoy Light Keypress-Delay'),_(u"Seconds of delay until the PipBoy Light switches on."),
        ('fPlayerPipBoyLightTimer',),
        (_('0.3'),0.3),
        (_('0.4'),0.4),
        (_('0.5'),0.5),
        (_('0.6'),0.6),
        (_('0.7'),0.7),
        (_('[0.8]'),0.8),
        (_('1.0'),1.0),
        (_(u'Custom'),0.8),
        ),
    (_(u'VATS Playback Delay'),_(u"Seconds of delay after the VATS Camera finished playback."),
        ('fVATSPlaybackDelay',),
        (_('0.01'),0.01),
        (_('0.05'),0.05),
        (_('0.10'),0.1),
        (_('[0.17]'),0.17),
        (_('0.25'),0.25),
        (_(u'Custom'),0.17),
        ),
    (_(u'NPC-Death XP Threshold (Followers)'),_(u"Percentage of total damage you have to inflict in order to get XP"),
        ('iXPDeathRewardHealthThreshold',),
        (_('0%'),0),
        (_('25%'),25),
        (_('[40%]'),40),
        (_('50%'),50),
        (_('75%'),75),
        (_(u'Custom'),40),
        ),
    (_(u'Hacking: Maximum Number of words'),_(u"The maximum number of words appearing in the terminal hacking mini-game."),
        ('iHackingMaxWords',),
        (_('1'),1),
        (_('4'),4),
        (_('8'),8),
        (_('12'),12),
        (_('16'),16),
        (_('[20]'),20),
        (_(u'Custom'),20),
        ),
    (_(u'Shell Camera Distance'),_(u"Maximum distance at which gun arisings (shell case, particle, decal) show from camera."),
        ('fGunParticleCameraDistance', 'fGunShellCameraDistance', 'fGunDecalCameraDistance'),
        (_('x 1.5'),2048.0*1.5, 512.0*1.5, 2048.0*1.5),
        (_('x 2'),  2048.0*2.0, 512.0*2.0, 2048.0*2.0),
        (_('x 3'),  2048.0*3.0, 512.0*3.0, 2048.0*3.0),
        (_('x 4'),  2048.0*4.0, 512.0*4.0, 2048.0*4.0),
        (_('x 5'),  2048.0*5.0, 512.0*5.0, 2048.0*5.0),
        (_(u'Custom'),2048, 512, 2048),
        ),
    (_(u'Shell Litter Time'),_(u"Time before shell cases fade away from cells."),
        ('fGunShellLifetime',),
        (_(u'[10 Seconds]'),10),
        (_(u'20 Seconds'),20),
        (_(u'30 Seconds'),30),
        (_(u'1 Minute'),60),
        (_(u'3 Minutes'),60*3),
        (_(u'5 Minutes'),60*5),
        (_(u'Custom (in seconds)'),10),
        ),
    (_(u'Shell Litter Count'),_(u"Maximum number of debris (shell case, etc) allowed in cell."),
        ('iDebrisMaxCount',),
        (_('[50]'),50),
        (_('100'),100),
        (_('500'),500),
        (_('1000'),1000),
        (_('3000'),3000),
        (_(u'Custom'),50),
        ),
    (_(u'Terminal Speed Adjustment'),_(u"The display speed at the time of terminal hacking."),
        ('iHackingDumpRate','iHackingInputRate','iHackingOutputRate','iHackingFlashOffDuration','iHackingFlashOnDuration','iComputersDisplayRateMenus','iComputersDisplayRateNotes'),
        (_('x 2'),1000,40,134,250,375,300,300),
        (_('x 4'),2000,80,268,125,188,600,600),
        (_('[x 6]'),3000,120,402,83,126,900,900),
        (_(u'Custom'),3000,120,402,83,126,900,900),
        ),
    (_(u'Drag: Max Moveable Weight'),_(u"Maximum weight to be able move things with the drag key."),
        ('fMoveWeightMax',),
        (_('1500'),1500.0),
        (_(u'[Default (150)]'),150),
        (_(u'Custom'),150),
        ),
    ]

#--Bash Tags supported by this game
# 'Body-F', 'Body-M', 'Body-Size-M', 'Body-Size-F', 'C.Climate', 'C.Light', 'C.Music', 'C.Name', 'C.RecordFlags',
# 'C.Owner', 'C.Water','Deactivate', 'Delev', 'Eyes', 'Factions', 'Relations', 'Filter', 'Graphics', 'Hair',
# 'IIM', 'Invent', 'Names', 'NoMerge', 'NpcFaces', 'R.Relations', 'Relev', 'Scripts', 'ScriptContents', 'Sound',
# 'Stats', 'Voice-F', 'Voice-M', 'R.Teeth', 'R.Mouth', 'R.Ears', 'R.Head', 'R.Attributes-F',
# 'R.Attributes-M', 'R.Skills', 'R.Description', 'Roads', 'Actors.Anims',
# 'Actors.AIData', 'Actors.DeathItem', 'Actors.AIPackages', 'Actors.AIPackagesForceAdd', 'Actors.Stats',
# 'Actors.ACBS', 'NPC.Class', 'Actors.CombatStyle', 'Creatures.Blood',
# 'NPC.Race','Actors.Skeleton', 'NpcFacesForceFullImport', 'MustBeActiveIfImported',
# 'Deflst', 'Destructible', 'WeaponMods'
allTags = sorted((
    u'C.Climate', u'C.Light', u'C.Music', u'C.Name', u'C.Owner', u'C.RecordFlags',
    u'C.Water', u'Deactivate', u'Deflst', u'Delev', u'Destructible', u'Factions',
    u'Filter', u'Graphics',  u'Invent', u'Names', u'NoMerge', u'Relations',
    u'Relev', u'Sound', u'Stats', u'WeaponMods',
    ))

# ActorImporter, AliasesPatcher, AssortedTweaker, CellImporter, ContentsChecker,
# DeathItemPatcher, DestructiblePatcher, FidListsMerger, GlobalsTweaker,
# GmstTweaker, GraphicsPatcher, ImportFactions, ImportInventory, ImportRelations,
# ImportScriptContents, ImportScripts, KFFZPatcher, ListsMerger, NamesPatcher,
# NamesTweaker, NPCAIPackagePatcher, NpcFacePatcher, PatchMerger, RacePatcher,
# RoadImporter, SoundPatcher, StatsPatcher, UpdateReferences, WeaponModsPatcher,
#--Patcher available when building a Bashed Patch (referenced by class name)
patchers = (
    u'AliasesPatcher', u'CellImporter', u'DestructiblePatcher', u'FidListsMerger',
    u'GmstTweaker', u'ImportFactions', u'ImportInventory', u'ImportRelations',
    u'ListsMerger', u'NamesPatcher', u'PatchMerger', 'SoundPatcher', u'StatsPatcher',
    u'WeaponModsPatcher',
    )

#--CBash patchers available when building a Bashed Patch
CBash_patchers = (
)
#-------------------------------------------------------------------------------
# ListsMerger
#-------------------------------------------------------------------------------
listTypes = ('LVLC','LVLI','LVLN')
#-------------------------------------------------------------------------------
# NamesPatcher
#-------------------------------------------------------------------------------
namesTypes = set((
    'ACTI','ALCH','AMMO','ARMO','BOOK','CCRD','CHIP','CLAS','CMNY','CONT','CREA',
    'CSNO','DOOR','EYES','FACT','HAIR','IMOD','INGR','KEYM','LIGH','MISC','NOTE',
    'NPC_','RACE','RCCT','RCPE','REPU','SPEL','TACT','TERM','WEAP',
    ))
#-------------------------------------------------------------------------------
# ItemPrices Patcher
#-------------------------------------------------------------------------------
pricesTypes = {'ALCH':{},'AMMO':{},'ARMO':{},'ARMA':{},'BOOK':{},'INGR':{},'KEYM':{},'LIGH':{},'MISC':{},'WEAP':{}}

#-------------------------------------------------------------------------------
# StatsImporter
#-------------------------------------------------------------------------------
statsTypes = {
        'ALCH':('eid', 'weight', 'value'),
        'AMMO':('eid', 'weight', 'value', 'speed', 'clipRounds','projPerShot'),
        'ARMA':('eid', 'weight', 'value', 'health', 'ar','dt'),
        'ARMO':('eid', 'weight', 'value', 'health', 'ar','dt'),
        'BOOK':('eid', 'weight', 'value'),
        'INGR':('eid', 'weight', 'value'),
        'KEYM':('eid', 'weight', 'value'),
        'LIGH':('eid', 'weight', 'value', 'duration'),
        'MISC':('eid', 'weight', 'value'),
        'WEAP':('eid', 'weight', 'value', 'health', 'damage','clipsize',
                'animationMultiplier','reach','ammoUse','minSpread','spread','sightFov','baseVatsToHitChance','projectileCount',
                'minRange','maxRange','animationAttackMultiplier','fireRate','overrideActionPoint','rumbleLeftMotorStrength',
                'rumbleRightMotorStrength','rumbleDuration','overrideDamageToWeaponMult','attackShotsPerSec',
                'reloadTime','jamTime','aimArc','rambleWavelangth','limbDmgMult','sightUsage',
                'semiAutomaticFireDelayMin','semiAutomaticFireDelayMax',
                'strengthReq','regenRate','killImpulse','impulseDist','skillReq',
                'criticalDamage','criticalMultiplier',
                'vatsSkill','vatsDamMult','vatsAp'),
    }
statsHeaders = (
        #--Alch
        (u'ALCH',
            (u'"' + '","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
            _(u'Editor Id'),_(u'Weight'),_(u'Value'))) + u'"\n')),
        #Ammo
        (u'AMMO',
            (u'"' + u'","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
            _(u'Editor Id'),_(u'Weight'),_(u'Value'),_(u'Speed'),_(u'Clip Rounds'),_(u'Proj/Shot'))) + u'"\n')),
        #--Armor
        (u'ARMO',
            (u'"' + u'","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
            _(u'Editor Id'),_(u'Weight'),_(u'Value'),_(u'Health'),_(u'AR'),_(u'DT'))) + u'"\n')),
        #--Armor Addon
        (u'ARMA',
            (u'"' + u'","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
            _(u'Editor Id'),_(u'Weight'),_(u'Value'),_(u'Health'),_(u'AR'),_(u'DT'))) + '"\n')),
        #Books
        (u'BOOK',
            (u'"' + u'","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
            _(u'Editor Id'),_(u'Weight'),_(u'Value'))) + u'"\n')),
        #Ingredients
        (u'INGR',
            (u'"' + u'","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
           _(u'Editor Id'),_(u'Weight'),_(u'Value'))) + u'"\n')),
        #--Keys
        (u'KEYM',
            (u'"' + u'","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
            _(u'Editor Id'),_(u'Weight'),_(u'Value'))) + u'"\n')),
        #Lights
        (u'LIGH',
            (u'"' + u'","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
            _(u'Editor Id'),_(u'Weight'),_(u'Value'),_(u'Duration'))) + u'"\n')),
        #--Misc
        (u'MISC',
            (u'"' + u'","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
            _(u'Editor Id'),_(u'Weight'),_(u'Value'))) + u'"\n')),
        #--Weapons
        (u'WEAP',
            (u'"' + u'","'.join((_(u'Type'),_(u'Mod Name'),_(u'ObjectIndex'),
            _(u'Editor Id'),_(u'Weight'),_(u'Value'),_(u'Health'),_(u'Damage'),
            _(u'Clip Size'),_(u'Animation Multiplier'),_(u'Reach'),_(u'Ammo Use'),
            _(u'Min Spread'),_(u'Spread'),_(u'Sight Fov'),
            _(u'Base VATS To-Hit Chance'), _(u'Projectile Count'),_(u'Min Range'),
            _(u'Max Range'), _(u'Animation Attack Multiplier'), _(u'Fire Rate'),
            _(u'Override - Action Point'), _(u'Rumble - Left Motor Strength'),
            _(u'rRmble - Right Motor Strength'), _(u'Rumble - Duration'),
            _(u'Override - Damage To Weapon Mult'), _(u'Attack Shots/Sec'),
            _(u'Reload Time'), _(u'Jam Time'), _(u'Aim Arc'), _(u'Ramble - Wavelangth'),
            _(u'Limb Dmg Mult'), _(u'Sight Usage'),_(u'Semi-Automatic Fire Delay Min'),
            _(u'Semi-Automatic Fire Delay Max'),_(u'Strength Req'), _(u'Regen Rate'),
            _(u'Kill Impulse'), _(u'Impulse Dist'), _(u'Skill Req'),_(u'Critical Damage'),
            _(u'Crit % Mult'),_(u'VATS Skill'), _(u'VATS Dam. Mult'),
            _(u'VATS AP'))) + u'"\n')),
        )

#-------------------------------------------------------------------------------
# SoundPatcher
#-------------------------------------------------------------------------------
# Needs longs in SoundPatcher
soundsLongsTypes = set((
    'ACTI', 'ADDN', 'ALCH', 'ASPC', 'CONT', 'CREA', 'DOOR', 'LIGH', 'MGEF', 'SOUN',
    'WATR', 'WTHR', 'WEAP', 'TACT',
))
soundsTypes = {
    "ACTI": ('soundLooping','soundActivation',),
    "ADDN": ('ambientSound',),
    "ALCH": ('dropSound','pickupSound','soundConsume',),
    "ASPC": ('soundLooping','useSoundFromRegion',),
    "CONT": ('soundOpen','soundClose','soundRandomLooping',),
    "CREA": ('footWeight','inheritsSoundsFrom','sounds'),
    "DOOR": ('soundOpen','soundClose','soundLoop',),
    "LIGH": ('sound',),
    "MGEF": ('castingSound','boltSound','hitSound','areaSound',),
#    "REGN": ('entries.sounds',),
    "SOUN": ('soundFile','minDist','maxDist','freqAdj','staticAtten',
             'stopTime','startTime','point0','point1','point2','point3',
             'point4','reverb','priority','xLoc','yLoc',),
    "WATR": ('sound',),
    "WTHR": ('sounds',),
    "WEAP": ('pickupSound','dropSound','soundGunShot3D','soundGunShot2D',
             'soundGunShot3DLooping','soundMeleeSwingGunNoAmmo','soundBlock','idleSound',
             'equipSound','unequipSound','soundMod1Shoot3Ds','soundMod1Shoot2D',
             'soundLevel',),
}
soundsFidTypes = {
    "TACT": ('sound',),
}

#-------------------------------------------------------------------------------
# CellImporter
#-------------------------------------------------------------------------------
cellAutoKeys = (
    u'C.Acoustic',u'C.Climate',u'C.Encounter',u'C.ImageSpace',u'C.Light',
    u'C.LTemplate',u'C.Music',u'C.Name',u'C.Owner',u'C.RecordFlags',u'C.Water',)#,u'C.Maps')
cellRecAttrs = {
            u'C.Acoustic': ('acousticSpace',),
            u'C.Climate': ('climate',),
            u'C.Encounter': ('encounterZone',),
            u'C.ImageSpace': ('imageSpace',),
            u'C.Light': ('ambientRed','ambientGreen','ambientBlue','unused1',
                        'directionalRed','directionalGreen','directionalBlue','unused2',
                        'fogRed','fogGreen','fogBlue','unused3',
                        'fogNear','fogFar','directionalXY','directionalZ',
                        'directionalFade','fogClip',),
            u'C.LTemplate': ('lightTemplate',),
            u'C.Music': ('music',),
            u'C.Name': ('full',),
            u'C.Owner': ('ownership',),
            u'C.RecordFlags': ('flags1',), # Yes seems funky but thats the way it is
            u'C.Water': ('water','waterHeight',),
            }
cellRecFlags = {
            u'C.Acoustic': '',
            u'C.Climate': 'behaveLikeExterior',
            u'C.Encounter': '',
            u'C.ImageSpace': '',
            u'C.Light': '',
            u'C.LTemplate': '',
            u'C.Music': '',
            u'C.Name': '',
            u'C.Owner': 'publicPlace',
            u'C.RecordFlags': '',
            u'C.Water': 'hasWater',
            }
#-------------------------------------------------------------------------------
# GraphicsPatcher
#-------------------------------------------------------------------------------
graphicsLongsTypes = set((
    'ACTI', 'ALCH', 'AMMO', 'ARMA', 'ARMO', 'BOOK', 'CLAS', 'CREA', 'DOOR', 'EFSH',
    'FURN', 'GRAS', 'INGR', 'KEYM', 'LIGH', 'LSCR', 'LTEX', 'MGEF', 'MISC', 'STAT',
    'TREE', 'WEAP', 'MGEF',
    ))
graphicsTypes = {
    "ACTI": ('model',),
    "ALCH": ('iconPath','model',),
    "AMMO": ('iconPath','model',),
    "ARMA": ('maleBody','maleWorld','maleIconPath','femaleBody','femaleWorld','femaleIconPath',),
    "ARMO": ('maleBody','maleWorld','maleIconPath','femaleBody','femaleWorld','femaleIconPath',),
    "BOOK": ('iconPath','model',),
    "CLAS": ('iconPath',),
    "CREA": ('bodyParts','nift_p',),
    "DOOR": ('model',),
    "EFSH": ('flags','unused1','memSBlend',
    'memBlendOp','memZFunc','fillRed','fillGreen','fillBlue',
    'unused2','fillAIn','fillAFull','fillAOut','fillAPRatio',
    'fillAAmp','fillAFreq','fillAnimSpdU','fillAnimSpdV','edgeOff',
    'edgeRed','edgeGreen','edgeBlue','unused3','edgeAIn',
    'edgeAFull','edgeAOut','edgeAPRatio','edgeAAmp','edgeAFreq',
    'fillAFRatio','edgeAFRatio','memDBlend','partSBlend',
    'partBlendOp','partZFunc','partDBlend','partBUp',
    'partBFull','partBDown','partBFRatio',
    'partBPRatio','partLTime','partLDelta',
    'partNSpd','partNAcc','partVel1','partVel2',
    'partVel3','partAcc1','partAcc2','partAcc3',
    'partKey1','partKey2','partKey1Time',
    'partKey2Time','key1Red','key1Green',
    'key1Blue','unused4','key2Red','key2Green',
    'key2Blue','unused5','key3Red','key3Green',
    'key3Blue','unused6','key1A','key2A',
    'key3A','key1Time','key2Time','key3Time',
    'partNSpdDelta','partRot',
    'partRotDelta','partRotSpeed',
    'partRotSpeedDelta',FID,'addonModels',
    'holesStartTime','holesEndTime',
    'holesStartVal','holesEndVal',
    'edgeWidth','edgeRed','edgeGreen',
    'edgeBlue','unused7','explosionWindSpeed',
    'textureCountU','textureCountV',
    'addonModelsFadeInTime','addonModelsFadeOutTime',
    'addonModelsScaleStart','addonModelsScaleEnd',
    'addonModelsScaleInTime','addonModelsScaleOutTime',),
    "FURN": ('model',),
    "GRAS": ('model',),
    "INGR": ('iconPath','model',),
    "KEYM": ('iconPath','model',),
    "LIGH": ('iconPath','model',),
    "LSCR": ('iconPath',),
    "LTEX": ('iconPath',),
    "MGEF": ('iconPath','model',),
    "MISC": ('iconPath','model',),
    "STAT": ('model',),
    "TREE": ('iconPath','model',),
    "WEAP": ('iconPath','model',),
}
graphicsFidTypes = {
    "MGEF": ('effectShader','light','objectDisplayShader','cefEnchantment',)
}
#-------------------------------------------------------------------------------
# Inventory Patcher
#-------------------------------------------------------------------------------
inventoryTypes = ('CREA','NPC_','CONT',)
#-------------------------------------------------------------------------------
# Mod Record Elements ----------------------------------------------------------
#-------------------------------------------------------------------------------
FID = 'FID' #--Used by MelStruct classes to indicate fid elements.

# Magic Info ------------------------------------------------------------------
weaponTypes = (
    _(u'Big gun'),
    _(u'Energy'),
    _(u'Small gun'),
    _(u'Melee'),
    _(u'Unarmed'),
    _(u'Thrown'),
    _(u'Mine'),
    )

# Race Info -------------------------------------------------------------------
raceNames = {
    0x000019 : _(u'Caucasian'),
    0x0038e5 : _(u'Hispanic'),
    0x0038e6 : _(u'Asian'),
    0x003b3e : _(u'Ghoul'),
    0x00424a : _(u'AfricanAmerican'),
    0x0042be : _(u'AfricanAmerican Child'),
    0x0042bf : _(u'AfricanAmerican Old'),
    0x0042c0 : _(u'Asian Child'),
    0x0042c1 : _(u'Asian Old'),
    0x0042c2 : _(u'Caucasian Child'),
    0x0042c3 : _(u'Caucasian Old'),
    0x0042c4 : _(u'Hispanic Child'),
    0x0042c5 : _(u'Hispanic Old'),
    0x04bb8d : _(u'Caucasian Raider'),
    0x04bf70 : _(u'Hispanic Raider'),
    0x04bf71 : _(u'Asian Raider'),
    0x04bf72 : _(u'AfricanAmerican Raider'),
    0x0987dc : _(u'Hispanic Old Aged'),
    0x0987dd : _(u'Asian Old Aged'),
    0x0987de : _(u'AfricanAmerican Old Aged'),
    0x0987df : _(u'Caucasian Old Aged'),
    }

raceShortNames = {
    0x000019 : u'Cau',
    0x0038e5 : u'His',
    0x0038e6 : u'Asi',
    0x003b3e : u'Gho',
    0x00424a : u'Afr',
    0x0042be : u'AfC',
    0x0042bf : u'AfO',
    0x0042c0 : u'AsC',
    0x0042c1 : u'AsO',
    0x0042c2 : u'CaC',
    0x0042c3 : u'CaO',
    0x0042c4 : u'HiC',
    0x0042c5 : u'HiO',
    0x04bb8d : u'CaR',
    0x04bf70 : u'HiR',
    0x04bf71 : u'AsR',
    0x04bf72 : u'AfR',
    0x0987dc : u'HOA',
    0x0987dd : u'AOA',
    0x0987de : u'FOA',
    0x0987df : u'COA',
    }

raceHairMale = {
    0x000019 : 0x014b90, #--Cau
    0x0038e5 : 0x0a9d6f, #--His
    0x0038e6 : 0x014b90, #--Asi
    0x003b3e : None, #--Gho
    0x00424a : 0x0306be, #--Afr
    0x0042be : 0x060232, #--AfC
    0x0042bf : 0x0306be, #--AfO
    0x0042c0 : 0x060232, #--AsC
    0x0042c1 : 0x014b90, #--AsO
    0x0042c2 : 0x060232, #--CaC
    0x0042c3 : 0x02bfdb, #--CaO
    0x0042c4 : 0x060232, #--HiC
    0x0042c5 : 0x02ddee, #--HiO
    0x04bb8d : 0x02bfdb, #--CaR
    0x04bf70 : 0x02bfdb, #--HiR
    0x04bf71 : 0x02bfdb, #--AsR
    0x04bf72 : 0x0306be, #--AfR
    0x0987dc : 0x0987da, #--HOA
    0x0987dd : 0x0987da, #--AOA
    0x0987de : 0x0987d9, #--FOA
    0x0987df : 0x0987da, #--COA
    }

raceHairFemale = {
    0x000019 : 0x05dc6b, #--Cau
    0x0038e5 : 0x05dc76, #--His
    0x0038e6 : 0x022e50, #--Asi
    0x003b3e : None, #--Gho
    0x00424a : 0x05dc78, #--Afr
    0x0042be : 0x05a59e, #--AfC
    0x0042bf : 0x072e39, #--AfO
    0x0042c0 : 0x05a5a3, #--AsC
    0x0042c1 : 0x072e39, #--AsO
    0x0042c2 : 0x05a59e, #--CaC
    0x0042c3 : 0x072e39, #--CaO
    0x0042c4 : 0x05a59e, #--HiC
    0x0042c5 : 0x072e39, #--HiO
    0x04bb8d : 0x072e39, #--CaR
    0x04bf70 : 0x072e39, #--HiR
    0x04bf71 : 0x072e39, #--AsR
    0x04bf72 : 0x072e39, #--AfR
    0x0987dc : 0x044529, #--HOA
    0x0987dd : 0x044529, #--AOA
    0x0987de : 0x044529, #--FOA
    0x0987df : 0x044529, #--COA
    }

#--Plugin format stuff
class esp:
    #--Wrye Bash capabilities
    canBash = True         # Can create Bashed Patches
    canCBash = False         # CBash can handle this game's records
    canEditHeader = True   # Can edit basic info in the TES4 record

    #--Valid ESM/ESP header versions
    ## These are the valid 'version' numbers for the game file headers
    validHeaderVersions = (0.94,1.32,1.33,1.34)

    #--Strings Files, Skyrim only
    stringsFiles = []

    #--Class to use to read the TES4 record
    ## This is the class name in bosh.py to use for the TES4 record when reading
    ## Example: 'MreTes4'
    # tes4ClassName = ''

    #--Information about the basic record header
    # class header:
    #     format = ''         # Format passed to struct.unpack to unpack the header
    #     size = 0            # Size of the record header
    #     attrs = tuple()     # List of attributes to set = the return of struct.unpack
    #     defaults = tuple()  # Default values for each of the above attributes

    #--Top types in FalloutNV order.
    topTypes = ['GMST', 'TXST', 'MICN', 'GLOB', 'CLAS', 'FACT', 'HDPT', 'HAIR', 'EYES',
        'RACE', 'SOUN', 'ASPC', 'MGEF', 'SCPT', 'LTEX', 'ENCH', 'SPEL', 'ACTI', 'TACT',
        'TERM', 'ARMO', 'BOOK', 'CONT', 'DOOR', 'INGR', 'LIGH', 'MISC', 'STAT', 'SCOL',
        'MSTT', 'PWAT', 'GRAS', 'TREE', 'FURN', 'WEAP', 'AMMO', 'NPC_', 'CREA', 'LVLC',
        'LVLN', 'KEYM', 'ALCH', 'IDLM', 'NOTE', 'COBJ', 'PROJ', 'LVLI', 'WTHR', 'CLMT',
        'REGN', 'NAVI', 'DIAL', 'QUST', 'IDLE', 'PACK', 'CSTY', 'LSCR', 'ANIO', 'WATR',
        'EFSH', 'EXPL', 'DEBR', 'IMGS', 'IMAD', 'FLST', 'PERK', 'BPTD', 'ADDN', 'AVIF',
        'RADS', 'CAMS', 'CPTH', 'VTYP', 'IPCT', 'IPDS', 'ARMA', 'ECZN', 'MESG', 'RGDL',
        'DOBJ', 'LGTM', 'MUSC', 'IMOD', 'REPU', 'RCPE', 'RCCT', 'CHIP', 'CSNO', 'LSCT',
        'MSET', 'ALOC', 'CHAL', 'AMEF', 'CCRD', 'CMNY', 'CDCK', 'DEHY', 'HUNG', 'SLPD',
        'CELL', 'WRLD',]
    #--Dict mapping 'ignored' top types to un-ignored top types
    topIgTypes = dict()

    #--Record Types: all recognized record types (not just the top types)
    recordTypes = set(topTypes + 'GRUP,TES4,ACHR,ACRE,INFO,LAND,NAVM,PGRE,PMIS,REFR'.split(','))


class RecordHeader(brec.BaseRecordHeader):
    size = 24 # Size in bytes of a record header

    def __init__(self,recType='TES4',size=0,arg1=0,arg2=0,arg3=0,extra=0):
        self.recType = recType
        self.size = size
        if recType == 'GRUP':
            self.label = arg1
            self.groupType = arg2
            self.stamp = arg3
        else:
            self.flags1 = arg1
            self.fid = arg2
            self.flags2 = arg3
        self.extra = extra

    @staticmethod
    def unpack(ins):
        """Returns a RecordHeader object by reading the input stream."""
        type,size,uint0,uint1,uint2,uint3 = ins.unpack('=4s5I',24,'REC_HEADER')
        #--Bad type?
        if type not in esp.recordTypes:
            raise brec.ModError(ins.inName,u'Bad header type: '+repr(type))
        #--Record
        if type != 'GRUP':
            pass
        #--Top Group
        elif uint1 == 0: #groupType == 0 (Top Type)
            str0 = struct.pack('I',uint0)
            if str0 in esp.topTypes:
                uint0 = str0
            elif str0 in esp.topIgTypes:
                uint0 = esp.topIgTypes[str0]
            else:
                raise brec.ModError(ins.inName,u'Bad Top GRUP type: '+repr(str0))
        #--Other groups
        return RecordHeader(type,size,uint0,uint1,uint2,uint3)

    def pack(self):
        """Return the record header packed into a bitstream to be written to file."""
        if self.recType == 'GRUP':
            if isinstance(self.label,str):
                return struct.pack('=4sI4sIII',self.recType,self.size,
                                   self.label,self.groupType,self.stamp,
                                   self.extra)
            elif isinstance(self.label,tuple):
                return struct.pack('=4sIhhIII',self.recType,self.size,
                                   self.label[0],self.label[1],self.groupType,
                                   self.stamp,self.extra)
            else:
                return struct.pack('=4s5I',self.recType,self.size,self.label,
                                   self.groupType,self.stamp,self.extra)
        else:
            return struct.pack('=4s5I',self.recType,self.size,self.flags1,
                               self.fid,self.flags2,self.extra)

# These eye variables have been refactored from the Wrye Flash version of bosh.py.
# Their Oblivion equivalents remain in Bash's bosh.py.
def getIdFunc(modName):
    return lambda x: (GPath(modName),x)
ob = getIdFunc(masterFiles[0])
standardEyes = [ob(x) for x in (0x4252,0x4253,0x4254,0x4255,0x4256)]

defaultEyes = {
    #--fallout3.esm
    ob(0x000019): #--Caucasian
        standardEyes,
    ob(0x0038e5): #--Hispanic
        standardEyes,
    ob(0x0038e6): #--Asian
        standardEyes,
    ob(0x003b3e): #--Ghoul
        [ob(0x35e4f)],
    ob(0x00424a): #--AfricanAmerican
        standardEyes,
    ob(0x0042be): #--AfricanAmerican Child
        standardEyes,
    ob(0x0042bf): #--AfricanAmerican Old
        standardEyes,
    ob(0x0042c0): #--Asian Child
        standardEyes,
    ob(0x0042c1): #--Asian Old
        standardEyes,
    ob(0x0042c2): #--Caucasian Child
        standardEyes,
    ob(0x0042c3): #--Caucasian Old
        standardEyes,
    ob(0x0042c4): #--Hispanic Child
        standardEyes,
    ob(0x0042c5): #--Hispanic Old
        standardEyes,
    ob(0x04bb8d): #--Caucasian Raider
        [ob(0x4cb10)],
    ob(0x04bf70): #--Hispanic Raider
        [ob(0x4cb10)],
    ob(0x04bf71): #--Asian Raider
        [ob(0x4cb10)],
    ob(0x04bf72): #--AfricanAmerican Raider
        [ob(0x4cb10)],
    ob(0x0987dc): #--Hispanic Old Aged
        standardEyes,
    ob(0x0987dd): #--Asian Old Aged
        standardEyes,
    ob(0x0987de): #--AfricanAmerican Old Aged
        standardEyes,
    ob(0x0987df): #--Caucasian Old Aged
        standardEyes,
    }

#------------------------------------------------------------------------------
# Record Elements    ----------------------------------------------------------
#------------------------------------------------------------------------------
class MreActor(MelRecord):
    """Creatures and NPCs."""

    def mergeFilter(self,modSet):
        """Filter out items that don't come from specified modSet.
        Filters spells, factions and items."""
        if not self.longFids: raise StateError(_("Fids not in long format"))
        self.spells = [x for x in self.spells if x[0] in modSet]
        self.factions = [x for x in self.factions if x.faction[0] in modSet]
        self.items = [x for x in self.items if x.item[0] in modSet]

#------------------------------------------------------------------------------
class MelBipedFlags(bolt.Flags):
    """Biped flags element. Includes biped flag set by default."""
    mask = 0xFFFF
    def __init__(self,default=0L,newNames=None):
        names = bolt.Flags.getNames(
            'head', 'hair', 'upperBody', 'leftHand', 'rightHand', 'weapon',
            'pipboy', 'backpack', 'necklace', 'headband', 'hat', 'eyeGlasses',
            'noseRing', 'earrings', 'mask', 'choker', 'mouthObject',
            'bodyAddOn1', 'bodyAddOn2', 'bodyAddOn3')
        if newNames: names.update(newNames)
        bolt.Flags.__init__(self,default,names)

#------------------------------------------------------------------------------
class MelConditions(MelStructs):
    """Represents a set of quest/dialog conditions. Difficulty is that FID state
    of parameters depends on function index."""
    def __init__(self):
        """Initialize."""
        MelStructs.__init__(self,'CTDA','=B3sfH2siiII','conditions',
            'operFlag',('unused1',null3),'compValue','ifunc',('unused2',null2),
            'param1','param2','runOn','reference')

    def getDefault(self):
        """Returns a default copy of object."""
        target = MelStructs.getDefault(self)
        target.form1234 = 'iiII'
        return target

    def hasFids(self,formElements):
        """Include self if has fids."""
        formElements.add(self)

    def loadData(self,record,ins,type,size,readId):
        """Reads data from ins into record attribute."""
        if type == 'CTDA':
            if size != 28 and size != 24 and size != 20:
                raise ModSizeError(ins.inName,readId,28,size,False)
        else:
            raise ModError(ins.inName,_(u'Unexpected subrecord: ')+readId)
        target = MelObject()
        record.conditions.append(target)
        target.__slots__ = self.attrs
        unpacked1 = ins.unpack('=B3sfH2s',12,readId)
        (target.operFlag,target.unused1,target.compValue,ifunc,target.unused2) = unpacked1
        #--Get parameters
        if ifunc not in allConditions:
            raise bolt.BoltError(u'Unknown condition function: %d\nparam1: %08X\nparam2: %08X' % (ifunc,ins.unpackRef(), ins.unpackRef()))
        # Form1 is Param1
        form1 = 'I' if ifunc in fid1Conditions else 'i'
        # Form2 is Param2
        form2 = 'I' if ifunc in fid2Conditions else 'i'
        # Form3 is runOn
        form3 = 'I'
        # Form4 is reference, this is a formID when runOn = 2
        form4 = 'I'
        if size == 28:
            form1234 = form1+form2+form3+form4
            unpacked2 = ins.unpack(form1234,16,readId)
            (target.param1,target.param2,target.runOn,target.reference) = unpacked2
        elif size == 24:
            form1234 = form1+form2+form3
            unpacked2 = ins.unpack(form1234,12,readId)
            (target.param1,target.param2,target.runOn) = unpacked2
            target.reference = null4
        elif size == 20:
            form1234 = form1+form2
            unpacked2 = ins.unpack(form1234,8,readId)
            (target.param1,target.param2) = unpacked2
            target.runOn = null4
            target.reference = null4
        else:
            raise ModSizeError(ins.inName,readId,28,size,False)
        (target.ifunc,target.form1234) = (ifunc,form1234)
        if self._debug:
            unpacked = unpacked1+unpacked2
            print u' ',zip(self.attrs,unpacked)
            if len(unpacked) != len(self.attrs):
                print u' ',unpacked

    def dumpData(self,record,out):
        """Dumps data from record to outstream."""
        for target in record.conditions:
            out.packSub('CTDA','=B3sfH2s'+target.form1234,
                target.operFlag, target.unused1, target.compValue,
                target.ifunc, target.unused2, target.param1, target.param2,
                target.runOn, target.reference)

    def mapFids(self,record,function,save=False):
        """Applies function to fids. If save is true, then fid is set
        to result of function."""
        for target in record.conditions:
            form1234 = target.form1234
            if form1234[0] == 'I':
                result = function(target.param1)
                if save: target.param1 = result
            if form1234[1] == 'I':
                result = function(target.param2)
                if save: target.param2 = result
            # runOn is intU32, never FID, and Enum in FNVEdit
            #0:Subject,1:Target,2:Reference,3:Combat Target,4:Linked Reference
            if len(form1234) > 3 and form1234[3] == 'I' and target.runOn == 2:
                result = function(target.reference)
                if save: target.reference = result

#------------------------------------------------------------------------------
class MelDestructible(MelGroup):
    """Represents a set of destruct record."""

    MelDestVatsFlags = Flags(0L,Flags.getNames(
        (0, 'vatsTargetable'),
        ))

    MelDestStageFlags = Flags(0L,Flags.getNames(
        (0, 'capDamage'),
        (1, 'disable'),
        (2, 'destroy'),
        ))

    def __init__(self,attr='destructible'):
        """Initialize elements."""
        MelGroup.__init__(self,attr,
            MelStruct('DEST','i2B2s','health','count',
                     (MelDestructible.MelDestVatsFlags,'flagsDest',0L),'unused'),
            MelGroups('stages',
                MelStruct('DSTD','=4Bi2Ii','health','index','damageStage',
                          (MelDestructible.MelDestStageFlags,'flagsDest',0L),'selfDamagePerSecond',
                          (FID,'explosion',None),(FID,'debris',None),'debrisCount'),
                MelString('DMDL','model'),
                MelBase('DMDT','dmdt'),
                MelBase('DSTF','footer'),
                ),
        )

#------------------------------------------------------------------------------
class MelEffects(MelGroups):
    """Represents ingredient/potion/enchantment/spell effects."""

    def __init__(self,attr='effects'):
        """Initialize elements."""
        MelGroups.__init__(self,attr,
            MelFid('EFID','baseEffect'),
            MelStruct('EFIT','4Ii','magnitude','area','duration','recipient','actorValue'),
            MelConditions(),
            )

#------------------------------------------------------------------------------
class MreHasEffects:
    """Mixin class for magic items."""
    def getEffects(self):
        """Returns a summary of effects. Useful for alchemical catalog."""
        effects = []
        avEffects = bush.genericAVEffects
        effectsAppend = effects.append
        for effect in self.effects:
            mgef, actorValue = effect.name, effect.actorValue
            if mgef not in avEffects:
                actorValue = 0
            effectsAppend((mgef,actorValue))
        return effects

    def getSpellSchool(self,mgef_school=bush.mgef_school):
        """Returns the school based on the highest cost spell effect."""
        spellSchool = [0,0]
        for effect in self.effects:
            school = mgef_school[effect.name]
            effectValue = bush.mgef_basevalue[effect.name]
            if effect.magnitude:
                effectValue *=  effect.magnitude
            if effect.area:
                effectValue *=  (effect.area/10)
            if effect.duration:
                effectValue *=  effect.duration
            if spellSchool[0] < effectValue:
                spellSchool = [effectValue,school]
        return spellSchool[1]

    def getEffectsSummary(self,mgef_school=None,mgef_name=None):
        """Return a text description of magic effects."""
        mgef_school = mgef_school or bush.mgef_school
        mgef_name = mgef_name or bush.mgef_name
        with bolt.sio() as buff:
            avEffects = bush.genericAVEffects
            aValues = bush.actorValues
            buffWrite = buff.write
            if self.effects:
                school = self.getSpellSchool(mgef_school)
                buffWrite(bush.actorValues[20+school] + u'\n')
            for index,effect in enumerate(self.effects):
                if effect.scriptEffect:
                    effectName = effect.scriptEffect.full or u'Script Effect'
                else:
                    effectName = mgef_name[effect.name]
                    if effect.name in avEffects:
                        effectName = re.sub(_(u'(Attribute|Skill)'),aValues[effect.actorValue],effectName)
                buffWrite(u'o+*'[effect.recipient]+u' '+effectName)
                if effect.magnitude: buffWrite(u' %sm'%effect.magnitude)
                if effect.area: buffWrite(u' %sa'%effect.area)
                if effect.duration > 1: buffWrite(u' %sd'%effect.duration)
                buffWrite(u'\n')
                return buff.getvalue()

#------------------------------------------------------------------------------
class MreLeveledList(MelRecord):
    """Leveled item/creature/spell list.."""
    _flags = Flags(0,Flags.getNames('calcFromAllLevels','calcForEachItem','useAllSpells'))
    #--Special load classes
    class MelLevListLvld(MelStruct):
        """Subclass to support alternate format."""
        def loadData(self,record,ins,type,size,readId):
            MelStruct.loadData(self,record,ins,type,size,readId)
            if record.chanceNone > 127:
                record.flags.calcFromAllLevels = True
                record.chanceNone &= 127

    class MelLevListLvlo(MelStruct):
        """Subclass to support alternate format."""
        def loadData(self,record,ins,type,size,readId):
            if size == 12:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 8:
                format,attrs = ('iI',('level','listId'))####might be h2sI
            else:
                raise "Unexpected size encountered for LVLO subrecord: %s" % size
            unpacked = ins.unpack(format,size,readId)
            setter = record.__setattr__
            for attr,value,action in zip(attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked
    #--Element Set
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelLevListLvld('LVLD','B','chanceNone'),
        MelStruct('LVLF','B',(_flags,'flags',0L)),
        MelFid('SCRI','script'),
        MelFid('TNAM','template'),
        MelFid('LVLG','glob'),
        MelGroups('entries',
                  MelLevListLvlo('LVLO','h2sIh2s','level',('unused1',null2),(FID,'listId',None),('count',1),('unused2',null2)),
                  MelOptStruct('COED','IIf',(FID,'owner',None),(FID,'glob',None),('condition',1.0)),
                  ),
        MelNull('DATA'),
        )
    __slots__ = (MelRecord.__slots__ + melSet.getSlotsUsed() +
        ['mergeOverLast','mergeSources','items','delevs','relevs'])

    def __init__(self,header,ins=None,unpack=False):
        """Initialize."""
        MelRecord.__init__(self,header,ins,unpack)
        self.mergeOverLast = False #--Merge overrides last mod merged
        self.mergeSources = None #--Set to list by other functions
        self.items  = None #--Set of items included in list
        self.delevs = None #--Set of items deleted by list (Delev and Relev mods)
        self.relevs = None #--Set of items relevelled by list (Relev mods)

    def mergeFilter(self,modSet):
        """Filter out items that don't come from specified modSet."""
        if not self.longFids: raise StateError(_("Fids not in long format"))
        self.entries = [entry for entry in self.entries if entry.listId[0] in modSet]

    def mergeWith(self,other,otherMod):
        """Merges newLevl settings and entries with self.
        Requires that: self.items, other.delevs and other.relevs be defined."""
        if not self.longFids: raise StateError(_("Fids not in long format"))
        if not other.longFids: raise StateError(_("Fids not in long format"))
        #--Relevel or not?
        if other.relevs:
            self.chanceNone = other.chanceNone
            self.script = other.script
            self.template = other.template
            self.flags = other.flags()
            self.glob = other.glob
        else:
            self.chanceNone = other.chanceNone or self.chanceNone
            self.script   = other.script or self.script
            self.template = other.template or self.template
            self.flags |= other.flags
            self.glob = other.glob or self.glob
        #--Remove items based on other.removes
        if other.delevs or other.relevs:
            removeItems = self.items & (other.delevs | other.relevs)
            self.entries = [entry for entry in self.entries if entry.listId not in removeItems]
            self.items = (self.items | other.delevs) - other.relevs
        hasOldItems = bool(self.items)
        #--Add new items from other
        newItems = set()
        entriesAppend = self.entries.append
        newItemsAdd = newItems.add
        for entry in other.entries:
            if entry.listId not in self.items:
                entriesAppend(entry)
                newItemsAdd(entry.listId)
        if newItems:
            self.items |= newItems
            self.entries.sort(key=attrgetter('listId','level','count','owner','condition'))
        #--Is merged list different from other? (And thus written to patch.)
        if (self.chanceNone != other.chanceNone or
            self.script != other.script or
            self.template != other.template or
            #self.flags != other.flags or
            self.glob != other.glob or
            len(self.entries) != len(other.entries)
            ):
            self.mergeOverLast = True
        else:
            otherlist = other.entries
            otherlist.sort(key=attrgetter('listId','level','count','owner','condition'))
            for selfEntry,otherEntry in zip(self.entries,otherlist):
                if (selfEntry.listId != otherEntry.listId or
                    selfEntry.level != otherEntry.level or
                    selfEntry.count != otherEntry.count or
                    selfEntry.owner != otherEntry.owner or
                    selfEntry.condition != otherEntry.condition):
                    self.mergeOverLast = True
                    break
            else:
                self.mergeOverLast = False
        if self.mergeOverLast:
            self.mergeSources.append(otherMod)
        else:
            self.mergeSources = [otherMod]
        #--Done
        self.setChanged(self.mergeOverLast)

#------------------------------------------------------------------------------
class MelMODS(MelBase):
    """MODS/MO2S/etc/DMDS subrecord"""
    def hasFids(self,formElements):
        """Include self if has fids."""
        formElements.add(self)

    def setDefault(self,record):
        """Sets default value for record instance."""
        record.__setattr__(self.attr,None)

    def loadData(self,record,ins,type,size,readId):
        """Reads data from ins into record attribute."""
        insUnpack = ins.unpack
        insRead32 = ins.readString32
        count, = insUnpack('I',4,readId)
        data = []
        dataAppend = data.append
        for x in xrange(count):
            string = ins.readString32(size,readId)
            fid = ins.unpackRef(readId)
            unk, = ins.unpack('I',4,readId)
            dataAppend((string,fid,unk))
        record.__setattr__(self.attr,data)

    def dumpData(self,record,out):
        """Dumps data from record to outstream."""
        data = record.__getattribute__(self.attr)
        if data is not None:
            structPack = struct.pack
            data = record.__getattribute__(self.attr)
            outData = structPack('I',len(data))
            for (string,fid,unk) in data:
                outData += structPack('I',len(string))
                outData += _encode(string)
                outData += structPack('=2I',fid,unk)
            out.packSub(self.subType,outData)

    def mapFids(self,record,function,save=False):
        """Applies function to fids.  If save is true, then fid is set
           to result of function."""
        attr = self.attr
        data = record.__getattribute__(attr)
        if data is not None:
            data = [(string,function(fid),unk) for (string,fid,unk) in record.__getattribute__(attr)]
            if save: record.__setattr__(attr,data)

#------------------------------------------------------------------------------
class MelModel(MelGroup):
    """Represents a model record."""
    typeSets = (
        ('MODL','MODB','MODT','MODS','MODD'),
        ('MOD2','MO2B','MO2T','MO2S','MO2D'),
        ('MOD3','MO3B','MO3T','MO3S','MOSD'),
        ('MOD4','MO4B','MO4T','MO4S','MO4D'),)

    def __init__(self,attr='model',index=0):
        """Initialize. Index is 0,2,3,4 for corresponding type id."""
        types = MelModel.typeSets[(0,index-1)[index>0]]
        MelGroup.__init__(self,attr,
            MelString(types[0],'modPath'),
            MelBase(types[1],'modb_p'), ### Bound Radius, Float
            MelBase(types[2],'modt_p'), ###Texture Files Hashes, Byte Array
            MelMODS(types[3],'mod_s'),
            MelBase(types[4],'modd_p'),)

    def debug(self,on=True):
        """Sets debug flag on self."""
        for element in self.elements[:2]: element.debug(on)
        return self

#------------------------------------------------------------------------------
class MelOwnership(MelGroup):
    """Handles XOWN, XRNK, and XGLB for cells and cell children."""

    def __init__(self,attr='ownership'):
        """Initialize."""
        MelGroup.__init__(self,attr,
            MelFid('XOWN','owner'),
            MelOptStruct('XRNK','i',('rank',None)),
            # Double check XGLB it's not used in FNVEdit
            MelFid('XGLB','global'),
        )

    def dumpData(self,record,out):
        """Dumps data from record to outstream."""
        if record.ownership and record.ownership.owner:
            MelGroup.dumpData(self,record,out)

#------------------------------------------------------------------------------
class MelScrxen(MelFids):
    """Handles mixed sets of SCRO and SCRV for scripts, quests, etc."""

    def getLoaders(self,loaders):
        loaders['SCRV'] = self
        loaders['SCRO'] = self

    def loadData(self,record,ins,type,size,readId):
        isFid = (type == 'SCRO')
        if isFid: value = ins.unpackRef(readId)
        else: value, = ins.unpack('I',4,readId)
        record.__getattribute__(self.attr).append((isFid,value))

    def dumpData(self,record,out):
        for isFid,value in record.__getattribute__(self.attr):
            if isFid: out.packRef('SCRO',value)
            else: out.packSub('SCRV','I',value)

    def mapFids(self,record,function,save=False):
        scrxen = record.__getattribute__(self.attr)
        for index,(isFid,value) in enumerate(scrxen):
            if isFid:
                result = function(value)
                if save: scrxen[index] = (isFid,result)

#------------------------------------------------------------------------------
# FalloutNV Records -----------------------------------------------------------
#------------------------------------------------------------------------------
class MreHeader(MreHeaderBase):
    """TES4 Record.  File header."""
    classType = 'TES4'

    #--Data elements
    melSet = MelSet(
        MelStruct('HEDR','f2I',('version',0.85),'numRecords',('nextObject',0xCE6)),
        MelBase('OFST','ofst_p',),  #--Obsolete?
        MelBase('DELE','dele_p',),  #--Obsolete?
        MelUnicode('CNAM','author',u'',512),
        MelUnicode('SNAM','description',u'',512),
        MreHeaderBase.MelMasterName('MAST','masters'),
        MelNull('DATA'), # 8 Bytes in Length
        MelFidList('ONAM','overrides'),
        MelBase('SCRN', 'scrn_p'),
        )
    __slots__ = MreHeaderBase.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAchr(MelRecord):
    """Placed NPC"""
    classType = 'ACHR'
    _flags = Flags(0L,Flags.getNames('oppositeParent','popIn'))
    _variableFlags = Flags(0L,Flags.getNames('isLongOrShort'))
    melSet=MelSet(
        MelString('EDID','eid'),
        MelFid('NAME','base'),
        MelFid('XEZN','encounterZone'),
        MelBase('XRGD','ragdollData'),
        MelBase('XRGB','ragdollBipedData'),
        MelGroup('patrolData',
            MelStruct('XPRD','f','idleTime'),
            MelBase('XPPA','patrolScriptMarker'),
            MelFid('INAM', 'idle'),
            MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            MelFid('TNAM','topic'),
            ),
        MelStruct('XLCM','i','levelModifier'),
        MelFid('XMRC','merchantContainer',),
        MelStruct('XCNT','i','count'),
        MelStruct('XRDS','f','radius',),
        MelStruct('XHLP','f','health',),
        MelStructs('XDCR','II','linkedDecals',(FID,'reference'),'unknown'), # ??
        MelFid('XLKR','linkedReference'),
        MelOptStruct('XCLP','8B','linkStartColorRed','linkStartColorGreen','linkStartColorBlue',('linkColorUnused1',null1),
                     'linkEndColorRed','linkEndColorGreen','linkEndColorBlue',('linkColorUnused2',null1)),
        MelGroup('activateParents',
            MelStruct('XAPD','B','flags'),
            MelStructs('XAPR','If','activateParentRefs',(FID,'reference'),'delay')
            ),
        MelString('XATO','activationPrompt'),
        MelOptStruct('XESP','IB3s',(FID,'parent'),(_flags,'parentFlags'),('unused1',null3)),
        MelOptStruct('XEMI','I',(FID,'emittance')),
        MelFid('XMBR','multiboundReference'),
        MelBase('XIBS','ignoredBySandbox'),
        MelOptStruct('XSCL','f',('scale',1.0)),
        MelOptStruct('DATA','=6f',('posX',None),('posY',None),('posZ',None),('rotX',None),('rotY',None),('rotZ',None)),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAcre(MelRecord):
    """Placed Creature"""
    classType = 'ACRE'
    _flags = Flags(0L,Flags.getNames('oppositeParent','popIn'))
    _variableFlags = Flags(0L,Flags.getNames('isLongOrShort'))
    melSet=MelSet(
        MelString('EDID','eid'),
        MelFid('NAME','base'),
        MelFid('XEZN','encounterZone'),
        MelBase('XRGD','ragdollData'),
        MelBase('XRGB','ragdollBipedData'),
        MelGroup('patrolData',
            MelStruct('XPRD','f','idleTime'),
            MelBase('XPPA','patrolScriptMarker'),
            MelFid('INAM', 'idle'),
            MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            MelFid('TNAM','topic'),
            ),
        MelStruct('XLCM','i','levelModifier'),
        MelOwnership(),
        MelFid('XMRC','merchantContainer'),
        MelStruct('XCNT','i','count'),
        MelStruct('XRDS','f','radius',),
        MelStruct('XHLP','f','health',),
        MelStructs('XDCR','II','linkedDecals',(FID,'reference'),'unknown'), # ??
        MelFid('XLKR','linkedReference'),
        MelOptStruct('XCLP','8B','linkStartColorRed','linkStartColorGreen','linkStartColorBlue',('linkColorUnused1',null1),
                     'linkEndColorRed','linkEndColorGreen','linkEndColorBlue',('linkColorUnused2',null1)),
        MelGroup('activateParents',
            MelStruct('XAPD','B','flags'),
            MelStructs('XAPR','If','activateParentRefs',(FID,'reference'),'delay')
            ),
        MelString('XATO','activationPrompt'),
        MelOptStruct('XESP','IB3s',(FID,'parent'),(_flags,'parentFlags'),('unused1',null3)),
        MelOptStruct('XEMI','I',(FID,'emittance')),
        MelFid('XMBR','multiboundReference'),
        MelBase('XIBS','ignoredBySandbox'),
        MelOptStruct('XSCL','f',('scale',1.0)),
        MelOptStruct('DATA','=6f',('posX',None),('posY',None),('posZ',None),('rotX',None),('rotY',None),('rotZ',None)),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreActi(MelRecord):
    """Activator record."""
    classType = 'ACTI'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelFid('SNAM','soundLooping'),
        MelFid('VNAM','soundActivation'),
        MelFid('INAM','radioTemplate'),
        MelFid('RNAM','radioStation'),
        MelFid('WNAM','waterType'),
        MelString('XATO','activationPrompt'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAddn(MelRecord):
    """Addon"""
    classType = 'ADDN'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelModel(),
        MelStruct('DATA','i','nodeIndex'),
        MelOptStruct('SNAM','I',(FID,'ambientSound')),
        MelStruct('DNAM','H2s','mastPartSysCap','unknown',),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAlch(MelRecord,MreHasEffects):
    """ALCH (potion) record."""
    classType = 'ALCH'
    _flags = Flags(0L,Flags.getNames('autoCalc','isFood','medicine',))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelFull0(),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        #-1:None,0:Big Guns,1:Energy Weapons,2:Small Guns,3:Melee Weapons,
        #4:Unarmed Weapon,5:Thrown Weapons,6:Mine,7:Body Wear,8:Head Wear,
        #9:Hand Wear,10:Chems,11:Stimpack,12:Food,13:Alcohol
        MelStruct('ETYP','i',('etype',-1)),
        MelStruct('DATA','f','weight'),
        MelStruct('ENIT','iB3sIfI','value',(_flags,'flags',0L),('unused1',null3),
                  (FID,'withdrawalEffect',None),'addictionChance',(FID,'soundConsume',None)),
        MelEffects(),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAloc(MelRecord):
    """Media location controller."""
    classType = 'ALOC'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelStruct('NAM1','I','flags'),
        MelStruct('NAM2','I','num2'),
        MelStruct('NAM3','I','nam3'),
        MelStruct('NAM4','f','locationDelay'),
        MelStruct('NAM5','I','dayStart'),
        MelStruct('NAM6','I','nightStart'),
        MelStruct('NAM7','f','retrigerDelay'),
        MelFids('HNAM','neutralSets'),
        MelFids('ZNAM','allySets'),
        MelFids('XNAM','friendSets'),
        MelFids('YNAM','enemySets'),
        MelFids('LNAM','locationSets'),
        MelFids('GNAM','battleSets'),
        MelFid('RNAM','conditionalFaction'),
        MelStruct('FNAM','I','fnam'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAmef(MelRecord):
    """Ammo effect record."""
    classType = 'AMEF'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelStruct('DATA','2If','type','operation','value'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAmmo(MelRecord):
    """Ammo (arrow) record."""
    classType = 'AMMO'
    _flags = Flags(0L,Flags.getNames('notNormalWeapon','nonPlayable'))
    class MelAmmoDat2(MelStruct):
        """Handle older truncated DAT2 for AMMO subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 20:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 12:
                unpacked = ins.unpack('IIf',size,readId)
            else:
                raise "Unexpected size encountered for AMMO:DAT2 subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        MelStruct('DATA','fB3sIB','speed',(_flags,'flags',0L),('unused1',null3),'value','clipRounds'),
        MelAmmoDat2('DAT2','IIfIf','projPerShot',(FID,'projectile',0L),'weight',(FID,'consumedAmmo'),'consumedPercentage'),
        MelString('ONAM','shortName'),
        MelString('QNAM','abbrev'),
        MelFids('RCIL','effects'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAnio(MelRecord):
    """Animation object record."""
    classType = 'ANIO'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelModel(),
        MelFid('DATA','animationId'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreArma(MelRecord):
    """Armor addon record."""
    classType = 'ARMA'
    _flags = MelBipedFlags(0L,Flags.getNames())
    _generalFlags = Flags(0L,Flags.getNames(
        ( 2,'hasBackpack'),
        ( 3,'medium'),
        (5,'powerArmor'),
        (6,'notPlayable'),
        (7,'heavyArmor')
    ))
    class MelArmaDnam(MelStruct):
        """Handle older truncated DNAM for ARMA subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 12:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 4:
                unpacked = ins.unpack('=HH',size,readId)
            else:
                raise "Unexpected size encountered for ARMA subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, record.flags.getTrueAttrs()
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelStruct('BMDT','=2I',(_flags,'bipedFlags',0L),(_generalFlags,'generalFlags',0L)),
        MelModel('maleBody'),
        MelModel('maleWorld',2),
        MelString('ICON','maleIconPath'),
        MelString('MICO','maleSmallIconPath'),
        MelModel('femaleBody',3),
        MelModel('femaleWorld',4),
        MelString('ICO2','femaleIconPath'),
        MelString('MIC2','femaleSmallIconPath'),
        #-1:None,0:Big Guns,1:Energy Weapons,2:Small Guns,3:Melee Weapons,
        #4:Unarmed Weapon,5:Thrown Weapons,6:Mine,7:Body Wear,8:Head Wear,
        #9:Hand Wear,10:Chems,11:Stimpack,12:Food,13:Alcohol
        MelStruct('ETYP','i',('etype',-1)),
        MelStruct('DATA','IIf','value','health','weight'),
        MelArmaDnam('DNAM','=HHfI','ar','flags','dt',('unknown',0L)),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreArmo(MelRecord):
    """Armor record."""
    classType = 'ARMO'
    _flags = MelBipedFlags(0L,Flags.getNames())
    _generalFlags = Flags(0L,Flags.getNames(
        (5,'powerArmor'),
        (6,'notPlayable'),
        (7,'heavyArmor')
    ))
    class MelArmoDnam(MelStruct):
        """Handle older truncated DNAM for ARMO subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 12:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 4:
                unpacked = ins.unpack('=HH',size,readId)
            else:
                raise "Unexpected size encountered for ARMO subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, record.flags.getTrueAttrs()

    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelFid('SCRI','script'),
        MelFid('EITM','objectEffect'),
        MelStruct('BMDT','=2I',(_flags,'bipedFlags',0L),(_generalFlags,'generalFlags',0L)),
        MelModel('maleBody'),
        MelModel('maleWorld',2),
        MelString('ICON','maleIconPath'),
        MelString('MICO','maleSmallIconPath'),
        MelModel('femaleBody',3),
        MelModel('femaleWorld',4),
        MelString('ICO2','femaleIconPath'),
        MelString('MIC2','femaleSmallIconPath'),
        MelString('BMCT','ragdollTemplatePath'),
        MelDestructible(),
        MelFid('REPL','repairList'),
        MelFid('BIPL','bipedModelList'),
        #-1:None,0:Big Guns,1:Energy Weapons,2:Small Guns,3:Melee Weapons,
        #4:Unarmed Weapon,5:Thrown Weapons,6:Mine,7:Body Wear,8:Head Wear,
        #9:Hand Wear,10:Chems,11:Stimpack,12:Food,13:Alcohol
        MelStruct('ETYP','i',('etype',-1)),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        MelStruct('DATA','=2if','value','health','weight'),
        MelArmoDnam('DNAM','=hHfI','ar','flags','dt',('unknown',0L)),
        MelStruct('BNAM','I',('overridesAnimationSound',0L)),
        MelStructs('SNAM','IB3sI','animationSounds',(FID,'sound'),'chance',('unused','\xb7\xe7\x0b'),'type'),
        MelFid('TNAM','animationSoundsTemplate'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAspc(MelRecord):
    """Acoustic space record."""
    classType = 'ASPC'
    isKeyedByEid = True # NULL fids are acceptible

    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelFids('SNAM','soundLooping'),
        MelStruct('WNAM','I','wallaTrigerCount'),
        MelFid('RDAT','useSoundFromRegion'),
        MelStruct('ANAM','I','environmentType'),
        MelStruct('INAM','I','isInterior'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreAvif(MelRecord):
    """ActorValue Information record."""
    classType = 'AVIF'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelString('DESC','description'),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelString('ANAM','shortName'),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreBook(MelRecord):
    """BOOK record."""
    classType = 'BOOK'
    _flags = Flags(0,Flags.getNames('isScroll','isFixed'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('SCRI','script'),
        MelString('DESC','text'),
        MelDestructible(),
        MelOptStruct('YNAM','I',(FID,'pickupSound')),
        MelOptStruct('ZNAM','I',(FID,'dropSound')),
        MelStruct('DATA', '=BbIf',(_flags,'flags',0L),('teaches',-1),'value','weight'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed() + ['modb']

#------------------------------------------------------------------------------
class MreBptd(MelRecord):
    """Body part data record."""
    classType = 'BPTD'
    _flags = Flags(0L,Flags.getNames('severable','ikData','ikBipedData',
        'explodable','ikIsHead','ikHeadtracking','toHitChanceAbsolute'))
    class MelBptdGroups(MelGroups):
        def loadData(self,record,ins,type,size,readId):
            """Reads data from ins into record attribute."""
            if type == self.type0:
                target = self.getDefault()
                record.__getattribute__(self.attr).append(target)
            else:
                targets = record.__getattribute__(self.attr)
                if targets:
                    target = targets[-1]
                elif type == 'BPNN': # for NVVoidBodyPartData, NVraven02
                    target = self.getDefault()
                    record.__getattribute__(self.attr).append(target)
            slots = []
            for element in self.elements:
                slots.extend(element.getSlotsUsed())
            target.__slots__ = slots
            self.loaders[type].loadData(target,ins,type,size,readId)
    melSet = MelSet(
        MelString('EDID','eid'),
        MelModel(),
        MelBptdGroups('bodyParts',
            MelString('BPTN','partName'),
            MelString('BPNN','nodeName'),
            MelString('BPNT','vatsTarget'),
            MelString('BPNI','ikDataStartNode'),
            MelStruct('BPND','f3Bb2BH2I2fi2I7f2I2B2sf','damageMult',
                      (_flags,'flags'),'partType','healthPercent','actorValue',
                      'toHitChance','explodableChancePercent',
                      'explodableDebrisCount',(FID,'explodableDebris',0L),
                      (FID,'explodableExplosion',0L),'trackingMaxAngle',
                      'explodableDebrisScale','severableDebrisCount',
                      (FID,'severableDebris',0L),(FID,'severableExplosion',0L),
                      'severableDebrisScale','goreEffectPosTransX',
                      'goreEffectPosTransY','goreEffectPosTransZ',
                      'goreEffectPosRotX','goreEffectPosRotY','goreEffectPosRotZ',
                      (FID,'severableImpactDataSet',0L),
                      (FID,'explodableImpactDataSet',0L),'severableDecalCount',
                      'explodableDecalCount',('unused',null2),
                      'limbReplacementScale'),
            MelString('NAM1','limbReplacementModel'),
            MelString('NAM4','goreEffectsTargetBone'),
            MelBase('NAM5','endMarker'),
            ),
        MelFid('RAGA','ragdoll'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCams(MelRecord):
    """Cams Type"""
    classType = 'CAMS'

    # DATA 'Action','Location','Target' is wbEnum
    # 'Action-Shoot',
    # 'Action-Fly',
    # 'Action-Hit',
    # 'Action-Zoom'

    # 'Location-Attacker',
    # 'Location-Projectile',
    # 'Location-Target',

    # 'Target-Attacker',
    # 'Target-Projectile',
    # 'Target-Target',

    CamsFlagsFlags = Flags(0L,Flags.getNames(
            (0, 'positionFollowsLocation'),
            (1, 'rotationFollowsTarget'),
            (2, 'dontFollowBone'),
            (3, 'firstPersonCamera'),
            (4, 'noTracer'),
            (5, 'startAtTimeZero'),
        ))

    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('DATA','eid'),
        MelModel(),
        MelStruct('DATA','4I6f','action','location','target',
                  (CamsFlagsFlags,'flags',0L),'timeMultPlayer',
                  'timeMultTarget','timeMultGlobal','maxTime','minTime',
                  'targetPctBetweenActors',),
        MelFid('MNAM','imageSpaceModifier',),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCcrd(MelRecord):
    """Caravan Card."""
    classType = 'CCRD'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('SCRI','script'),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        MelString('TX00','textureFace'),
        MelString('TX01','textureBack'),
        MelStructs('INTV','I','suitAndValue','value'),
        MelStruct('DATA','I','value'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCdck(MelRecord):
    """Caravan deck record."""
    classType = 'CDCK'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelFids('CARD','cards'),
        MelStruct('DATA','I','count'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCell(MelRecord):
    """Cell record."""
    classType = 'CELL'
    cellFlags = Flags(0L,Flags.getNames((0, 'isInterior'),(1,'hasWater'),(2,'invertFastTravel'),
        (3,'forceHideLand'),(5,'publicPlace'),(6,'handChanged'),(7,'behaveLikeExterior')))
    inheritFlags = Flags(0L,Flags.getNames('ambientColor','directionalColor','fogColor','fogNear','fogFar',
        'directionalRotation','directionalFade','clipDistance','fogPower'))
    class MelCoordinates(MelOptStruct):
        """Handle older truncated XCLC for CELL subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 12:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 8:
                unpacked = ins.unpack('ii',size,readId)
            else:
                raise "Unexpected size encountered for XCLC subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, record.flags.getTrueAttrs()
        def dumpData(self,record,out):
            if not record.flags.isInterior:
                MelOptStruct.dumpData(self,record,out)
    class MelCellXcll(MelOptStruct):
        """Handle older truncated XCLL for CELL subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 40:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 36:
                unpacked = ins.unpack('=3Bs3Bs3Bs2f2i2f',size,readId)
            else:
                raise "Unexpected size encountered for XCLL subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, record.flags.getTrueAttrs()
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelStruct('DATA','B',(cellFlags,'flags',0L)),
        MelCoordinates('XCLC','iiI',('posX',None),('posY',None),('forceHideLand',0L)),
        MelCellXcll('XCLL','=3Bs3Bs3Bs2f2i3f','ambientRed','ambientGreen','ambientBlue',
            ('unused1',null1),'directionalRed','directionalGreen','directionalBlue',
            ('unused2',null1),'fogRed','fogGreen','fogBlue',
            ('unused3',null1),'fogNear','fogFar','directionalXY','directionalZ',
            'directionalFade','fogClip','fogPower'),
        MelBase('IMPF','footstepMaterials'), #--todo rewrite specific class.
        MelFid('LTMP','lightTemplate'),
        MelOptStruct('LNAM','I',(inheritFlags,'lightInheritFlags',0L)),
        #--CS default for water is -2147483648, but by setting default here to -2147483649,
        #  we force the bashed patch to retain the value of the last mod.
        MelOptStruct('XCLW','f',('waterHeight',-2147483649)),
        MelString('XNAM','waterNoiseTexture'),
        MelFidList('XCLR','regions'),
        MelOptStruct('XCMT','B','xcmt_p'),
        MelFid('XCIM','imageSpace'),
        MelOptStruct('XCET','B','xcet_p'),
        MelFid('XEZN','encounterZone'),
        MelFid('XCCM','climate'),
        MelFid('XCWT','water'),
        MelOwnership(),
        MelFid('XCAS','acousticSpace'),
        MelFid('XCMO','music'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreChal(MelRecord):
    """Challenge record."""
    classType = 'CHAL'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelFid('SCRI','script'),
        MelString('DESC','description'),
        MelStruct('DATA','4I2s2s4s','type','threshold','flags','interval',
                  'dependOnType1','dependOnType2','dependOnType3'),
        MelFid('SNAM','dependOnType4'),
        MelFid('XNAM','dependOnType5'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreChip(MelRecord):
    """Casino Chip."""
    classType = 'CHIP'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelDestructible(),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreClas(MelRecord):
    """Class record."""
    classType = 'CLAS'
    _flags = Flags(0L,Flags.getNames(
        ( 0,'Playable'),
        ( 1,'Guard'),
        ))
    aiService = Flags(0L,Flags.getNames(
        (0,'weapons'),
        (1,'armor'),
        (2,'clothing'),
        (3,'books'),
        (4,'foods'),
        (5,'chems'),
        (6,'stimpacks'),
        (7,'lights'),
        (10,'miscItems'),
        (13,'potions'),
        (14,'training'),
        (16,'recharge'),
        (17,'repair'),))

        # trainSkill
        # -1, None
        #  0, Barter
        #  1, Big Guns (obsolete)
        #  2, Energy Weapons
        #  3, Explosives
        #  4, Lockpick
        #  5, Medicine
        #  6, Melee Weapons
        #  7, Repair
        #  8, Science
        #  9, Guns
        # 10, Sneak
        # 11, Speech
        # 12, Survival
        # 13, Unarmed

    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelString('DESC','description'),
        MelString('ICON','iconPath'),
        MelStruct('DATA','4i2IbB2s','tagSkill1','tagSkill2','tagSkill3',
            'tagSkill4',(_flags,'flags',0L),(aiService,'services',0L),
            ('trainSkill',-1),('trainLevel',0),('unused1',null2)),
        # MelTuple('ATTR','7B','attributes',[0]*7),
        MelStructA('ATTR','7B','attributes','strength','perception','endurance','charisma',
            'intelligence','agility','luck'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreClmt(MelRecord):
    """Climate record."""
    classType = 'CLMT'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStructA('WLST','IiI', 'Weather', (FID,'weather'), 'chance', (FID,'global')),
        MelString('FNAM','sunPath'),
        MelString('GNAM','glarePath'),
        MelModel(),
        MelStruct('TNAM','6B','riseBegin','riseEnd','setBegin','setEnd',
                  'volatility','phaseLength',),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCmny(MelRecord):
    """Caravan Money."""
    classType = 'CMNY'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        MelStruct('DATA','I','absoluteValue'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCobj(MelRecord):
    """Constructible Object record (recipies)"""
    classType = 'COBJ'

    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('SCRI','script'),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        MelStruct('DATA','if','value','weight'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCont(MelRecord):
    """Container record."""
    classType = 'CONT'
    _flags = Flags(0,Flags.getNames(None,'respawns'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelFid('SCRI','script'),
        MelGroups('items',
            MelStruct('CNTO','Ii',(FID,'item',None),('count',1)),
            MelOptStruct('COED','IIf',(FID,'owner',None),(FID,'glob',None),('condition',1.0)),
        ),
        MelDestructible(),
        MelStruct('DATA','=Bf',(_flags,'flags',0L),'weight'),
        MelFid('SNAM','soundOpen'),
        MelFid('QNAM','soundClose'),
        MelFid('RNAM','soundRandomLooping'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCpth(MelRecord):
    """Camera Path"""
    classType = 'CPTH'

    # DATA 'Camera Zoom' isn wbEnum
    # 0, 'Default, Must Have Camera Shots',
    # 1, 'Disable, Must Have Camera Shots',
    # 2, 'Shot List, Must Have Camera Shots',

    melSet = MelSet(
        MelString('EDID','eid'),
        MelConditions(),
        MelFidList('ANAM','relatedCameraPaths',),
        MelStruct('DATA','B','cameraZoom',),
        MelFids('SNAM','cameraShots',),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCsno(MelRecord):
    """Casino."""
    classType = 'CSNO'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelStruct('DATA','2f9I2II','decksPercentBeforeShuffle','BlackjackPayoutRatio',
            'slotReel0','slotReel1','slotReel2','slotReel3','slotReel4','slotReel5','slotReel6',
            'numberOfDecks','maxWinnings',(FID,'currency'),(FID,'casinoWinningQuest'),'flags'),
        MelGroups('chipModels',
            MelString('MODL','model')),
        MelString('MOD2','slotMachineModel'),
        MelString('MOD3','blackjackTableModel'),
        MelString('MOD4','rouletteTableModel'),
        MelGroups('slotReelTextures',
            MelString('ICON','texture')),
        MelGroups('blackjackDecks',
            MelString('ICO2','texture')),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCrea(MreActor):
    """Creature Record."""
    classType = 'CREA'
    #--Main flags
    _flags = Flags(0L,Flags.getNames(
        ( 0,'biped'),
        ( 1,'essential'),
        ( 2,'weaponAndShield'),
        ( 3,'respawn'),
        ( 4,'swims'),
        ( 5,'flies'),
        ( 6,'walks'),
        ( 7,'pcLevelOffset'),
        ( 9,'noLowLevel'),
        (11,'noBloodSpray'),
        (12,'noBloodDecal'),
        (15,'noHead'),
        (16,'noRightArm'),
        (17,'noLeftArm'),
        (18,'noCombatInWater'),
        (19,'noShadow'),
        (20,'noVATSMelee'),
        (21,'allowPCDialogue'),
        (22,'cantOpenDoors'),
        (23,'immobile'),
        (24,'tiltFrontBack'),
        (25,'tiltLeftRight'),
        (26,'noKnockDown'),
        (27,'notPushable'),
        (28,'allowPickpocket'),
        (29,'isGhost'),
        (30,'noRotatingHeadTrack'),
        (31,'invulnerable'),))
    #--AI Service flags
    aiService = Flags(0L,Flags.getNames(
        (0,'weapons'),
        (1,'armor'),
        (2,'clothing'),
        (3,'books'),
        (4,'foods'),
        (5,'chems'),
        (6,'stimpacks'),
        (7,'lights'),
        (10,'miscItems'),
        (13,'potions'),
        (14,'training'),
        (16,'recharge'),
        (17,'repair'),))
    aggroflags = Flags(0L,Flags.getNames('aggroRadiusBehavior',))

    #--Mel Set
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelFids('SPLO','spells'),
        MelFid('EITM','effect'),
        MelStruct('EAMT','H', 'eamt'),
        MelStrings('NIFZ','bodyParts'),
        MelBase('NIFT','nift_p'), ###Texture File hashes, Byte Array
        MelStruct('ACBS','=I2Hh3HfhH',(_flags,'flags',0L),'fatigue',
            'barterGold',('level',1),'calcMin','calcMax','speedMultiplier',
            'karma','dispotionBase','templateFlags'),
        MelStructs('SNAM','=IB3s','factions',
            (FID,'faction',None),'rank',('unused1','IFZ')),
        MelFid('INAM','deathItem'),
        MelFid('VTCK','voice'),
        MelFid('TPLT','template'),
        MelDestructible(),
        MelFid('SCRI','script'),
        MelGroups('items',
            MelStruct('CNTO','Ii',(FID,'item',None),('count',1)),
            MelOptStruct('COED','IIf',(FID,'owner',None),(FID,'glob',None),
                ('condition',1.0)),
        ),
        MelStruct('AIDT','=5B3sIbBbBi',
        #0:Unaggressive,1:Aggressive,2:Very Aggressive,3:Frenzied
        ('aggression',0),
        #0:Cowardly,1:Cautious,2:Average,3:Brave,4:Foolhardy
        ('confidence',2),
        ('energyLevel',50),('responsibility',50),
        #0:Neutral,1:Afraid,2:Annoyed,3:Cocky,4:Drugged,5:Pleasant,6:Angry,7:Sad
        ('mood',0),
        ('unused_aidt',null3),(aiService,'services',0L),
        #-1:None,0:Barter,1:Big Guns (obsolete),2:Energy Weapons,3:Explosives
        #4:Lockpick,5:Medicine,6:Melee Weapons,7:Repair,8:Science,9:Guns,10:Sneak
        #11:Speech,12:Survival,13:Unarmed,
        ('trainSkill',-1),
        'trainLevel',
        #0:Helps Nobody,1:Helps Allies,2:Helps Friends and Allies
        ('assistance',0),
        (aggroflags,'aggroRadiusBehavior',0L),'aggroRadius'),
        MelFids('PKID','aiPackages'),
        MelStrings('KFFZ','animations'),
        MelStruct('DATA','=4Bh2sh7B','type','combatSkill','magicSkill',
            'stealthSkill','health',('unused2',null2),'damage','strength','perception',
            'endurance','charisma','intelligence','agility','luck'),
        MelStruct('RNAM','B','attackReach'),
        MelFid('ZNAM','combatStyle'),
        MelFid('PNAM','bodyPartData'),
        MelStruct('TNAM','f','turningSpeed'),
        MelStruct('BNAM','f','baseScale'),
        MelStruct('WNAM','f','footWeight'),
        MelStruct('NAM4','I',('impactMaterialType',0L)),
        MelStruct('NAM5','I',('soundLevel',0L)),
        MelFid('CSCR','inheritsSoundsFrom'),
        MelGroups('sounds',
            MelStruct('CSDT','I','type'),
            MelFid('CSDI','sound'),
            MelStruct('CSDC','B','chance'),
        ),
        MelFid('CNAM','impactDataset'),
        MelFid('LNAM','meleeWeaponList'),
        )
    __slots__ = MreActor.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreCsty(MelRecord):
    """CSTY Record. Combat Styles."""
    classType = 'CSTY'
    _flagsA = Flags(0L,Flags.getNames(
        ( 0,'advanced'),
        ( 1,'useChanceForAttack'),
        ( 2,'ignoreAllies'),
        ( 3,'willYield'),
        ( 4,'rejectsYields'),
        ( 5,'fleeingDisabled'),
        ( 6,'prefersRanged'),
        ( 7,'meleeAlertOK'),
        ))

    #--Mel Set
    melSet = MelSet(
        MelString('EDID','eid'),
        MelOptStruct('CSTD', '2B2s8f2B2s3fB3s2f5B3s2fH2s2B2sf','dodgeChance',
                    'lrChance',('unused1',null2),'lrTimerMin','lrTimerMax',
                    'forTimerMin','forTimerMax','backTimerMin','backTimerMax',
                    'idleTimerMin','idleTimerMax','blkChance','atkChance',
                    ('unused2',null2),'atkBRecoil','atkBunc','atkBh2h',
                    'pAtkChance',('unused3',null3),'pAtkBRecoil','pAtkBUnc',
                    'pAtkNormal','pAtkFor','pAtkBack','pAtkL','pAtkR',
                    ('unused4',null3),'holdTimerMin','holdTimerMax',
                    (_flagsA,'flagsA'),('unused5',null2),'acroDodge',
                    ('rushChance',25),('unused6',null3),('rushMult',1.0),),
        MelOptStruct('CSAD', '21f', 'dodgeFMult', 'dodgeFBase', 'encSBase', 'encSMult',
                     'dodgeAtkMult', 'dodgeNAtkMult', 'dodgeBAtkMult', 'dodgeBNAtkMult',
                     'dodgeFAtkMult', 'dodgeFNAtkMult', 'blockMult', 'blockBase',
                     'blockAtkMult', 'blockNAtkMult', 'atkMult','atkBase', 'atkAtkMult',
                     'atkNAtkMult', 'atkBlockMult', 'pAtkFBase', 'pAtkFMult'),
        MelOptStruct('CSSD', '9f4sI5f', 'coverSearchRadius', 'takeCoverChance',
                     'waitTimerMin', 'waitTimerMax', 'waitToFireTimerMin',
                     'waitToFireTimerMax', 'fireTimerMin', 'fireTimerMax'
                     'rangedWeaponRangeMultMin','unknown1','weaponRestrictions',
                     'rangedWeaponRangeMultMax','maxTargetingFov','combatRadius',
                     'semiAutomaticFireDelayMultMin','semiAutomaticFireDelayMultMax'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreDebr(MelRecord):
    """Debris record."""
    classType = 'DEBR'

    dataFlags = bolt.Flags(0L,bolt.Flags.getNames('hasCollissionData'))
    class MelDebrData(MelStruct):
        subType = 'DATA'
        _elements = (('percentage',0),('modPath',null1),('flags',0),)
        def __init__(self):
            """Initialize."""
            self.attrs,self.defaults,self.actions,self.formAttrs = self.parseElements(*self._elements)
            self._debug = False
        def loadData(self,record,ins,type,size,readId):
            """Reads data from ins into record attribute."""
            data = ins.read(size,readId)
            (record.percentage,) = struct.unpack('B',data[0:1])
            record.modPath = data[1:-2]
            if data[-2] != null1:
                raise ModError(ins.inName,_('Unexpected subrecord: ')+readId)
            (record.flags,) = struct.unpack('B',data[-1])
        def dumpData(self,record,out):
            """Dumps data from record to outstream."""
            data = ''
            data += struct.pack('B',record.percentage)
            data += record.modPath
            data += null1
            data += struct.pack('B',record.flags)
            out.packSub('DATA',data)
    melSet = MelSet(
        MelString('EDID','eid'),
        MelGroups('models',
            MelDebrData(),
            MelBase('MODT','modt_p'),
        ),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreDehy(MelRecord):
    """Dehydration stage record."""
    classType = 'DEHY'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('DATA','2I','trigerThreshold',(FID,'actorEffect')),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreDial(MelRecord):
    """Dialog record."""
    classType = 'DIAL'
    _flags = Flags(0,Flags.getNames('rumors','toplevel',))
    class MelDialData(MelStruct):
        """Handle older truncated DATA for DIAL subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 2:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 1:
                unpacked = ins.unpack('B',size,readId)
            else:
                raise "Unexpected size encountered for DIAL subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, record.flags.getTrueAttrs()
    class MelDialDistributor(MelNull):
        def __init__(self):
            self._debug = False
        def getLoaders(self,loaders):
            """Self as loader for structure types."""
            for type in ('INFC','INFX',):
                loaders[type] = self
        def setMelSet(self,melSet):
            """Set parent melset. Need this so that can reassign loaders later."""
            self.melSet = melSet
            self.loaders = {}
            for element in melSet.elements:
                attr = element.__dict__.get('attr',None)
                if attr: self.loaders[attr] = element
        def loadData(self,record,ins,type,size,readId):
            if type in ('INFC', 'INFX'):
                quests = record.__getattribute__('quests')
                if quests:
                    element = self.loaders['quests']
                else:
                    if type == 'INFC':
                        element = self.loaders['bare_infc_p']
                    elif type == 'INFX':
                        element = self.loaders['bare_infx_p']
            element.loadData(record,ins,type,size,readId)

    melSet = MelSet(
        MelString('EDID','eid'),
        MelFid('INFC','bare_infc_p'),
        MelFid('INFX','bare_infx_p'),
        MelGroups('quests',
            MelFid('QSTI','quest'),
            MelGroups('unknown',
                MelFid('INFC','infc_p'),
                MelBase('INFX','infx_p'),
            ),
        ),
        MelString('FULL','full'),
        MelStruct('PNAM','f','priority'),
        MelString('TDUM','tdum_p'),
        MelDialData('DATA','BB','dialType',(_flags,'dialFlags',0L)),
        MelDialDistributor(),
     )
    melSet.elements[-1].setMelSet(melSet)

    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed() + ['infoStamp','infoStamp2','infos']

    def __init__(self,header,ins=None,unpack=False):
        """Initialize."""
        MelRecord.__init__(self,header,ins,unpack)
        self.infoStamp = 0 #--Stamp for info GRUP
        self.infoStamp2 = 0 #--Stamp for info GRUP
        self.infos = []

    def loadInfos(self,ins,endPos,infoClass):
        """Load infos from ins. Called from MobDials."""
        infos = self.infos
        recHead = ins.unpackRecHeader
        infosAppend = infos.append
        while not ins.atEnd(endPos,'INFO Block'):
            #--Get record info and handle it
            header = recHead()
            recType = header[0]
            if recType == 'INFO':
                info = infoClass(header,ins,True)
                infosAppend(info)
            else:
                raise ModError(ins.inName, _('Unexpected %s record in %s group.')
                    % (recType,"INFO"))

    def dump(self,out):
        """Dumps self., then group header and then records."""
        MreRecord.dump(self,out)
        if not self.infos: return
        # Magic number '24': size of Fallout New Vegas's record header
        # Magic format '4sIIIII': format for Fallout New Vegas's GRUP record
        size = 24 + sum([24 + info.getSize() for info in self.infos])
        out.pack('4sIIIII','GRUP',size,self.fid,7,self.infoStamp,self.infoStamp2)
        for info in self.infos: info.dump(out)

    def updateMasters(self,masters):
        """Updates set of master names according to masters actually used."""
        MelRecord.updateMasters(self,masters)
        for info in self.infos:
            info.updateMasters(masters)

    def convertFids(self,mapper,toLong):
        """Converts fids between formats according to mapper.
        toLong should be True if converting to long format or False if converting to short format."""
        MelRecord.convertFids(self,mapper,toLong)
        for info in self.infos:
            info.convertFids(mapper,toLong)

#------------------------------------------------------------------------------
class MreDobj(MelRecord):
    """Default object manager record."""
    classType = 'DOBJ'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('DATA','34I',(FID,'stimpack'),(FID,'superStimpack'),(FID,'radX'),(FID,'radAway'),
            (FID,'morphine'),(FID,'perkParalysis'),(FID,'playerFaction'),(FID,'mysteriousStrangerNpc'),
            (FID,'mysteriousStrangerFaction'),(FID,'defaultMusic'),(FID,'battleMusic'),(FID,'deathMusic'),
            (FID,'successMusic'),(FID,'levelUpMusic'),(FID,'playerVoiceMale'),(FID,'playerVoiceMaleChild'),
            (FID,'playerVoiceFemale'),(FID,'playerVoiceFemaleChild'),(FID,'eatPackageDefaultFood'),
            (FID,'everyActorAbility'),(FID,'drugWearsOffImageSpace'),(FID,'doctersBag'),(FID,'missFortuneNpc'),
            (FID,'missFortuneFaction'),(FID,'meltdownExplosion'),(FID,'unarmedForwardPA'),(FID,'unarmedBackwardPA'),
            (FID,'unarmedLeftPA'),(FID,'unarmedRightPA'),(FID,'unarmedCrouchPA'),(FID,'unarmedCounterPA'),
            (FID,'spotterEffect'),(FID,'itemDetectedEffect'),(FID,'cateyeMobileEffect'),),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreDoor(MelRecord):
    """Container record."""
    classType = 'DOOR'
    _flags = Flags(0,Flags.getNames(
        ( 1,'automatic'),
        ( 2,'hidden'),
        ( 3,'minimalUse'),
        ( 4,'slidingDoor',),
    ))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelFid('SNAM','soundOpen'),
        MelFid('ANAM','soundClose'),
        MelFid('BNAM','soundLoop'),
        MelStruct('FNAM','B',(_flags,'flags',0L)),
        #MelFids('TNAM','destinations'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreEczn(MelRecord):
    """Encounter Zone record."""
    classType = 'ECZN'
    _flags = Flags(0L,Flags.getNames('neverResets','matchPCBelowMinimumLevel'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('DATA','=I2bBs',(FID,'owner',None),'rank','minimumLevel',
                  (_flags,'flags',0L),('unused1',null1)),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreEfsh(MelRecord):
    """Effect shader record."""
    classType = 'EFSH'
    _flags = Flags(0L,Flags.getNames(
        ( 0,'noMemShader'),
        ( 3,'noPartShader'),
        ( 4,'edgeInverse'),
        ( 5,'memSkinOnly'),
        ))

    class MelEfshData(MelStruct):
        """Handle older truncated DATA for EFSH subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 308:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 300:
                unpacked = ins.unpack('B3s3I3Bs9f3Bs8f5I19f3Bs3Bs3Bs11fI5f3Bsf2I4f',size,readId)
            elif size == 284:
                unpacked = ins.unpack('B3s3I3Bs9f3Bs8f5I19f3Bs3Bs3Bs11fI5f3Bsf2I',size,readId)
            elif size == 248:
                unpacked = ins.unpack('B3s3I3Bs9f3Bs8f5I19f3Bs3Bs3Bs11fI',size,readId)
            elif size == 244:
                unpacked = ins.unpack('B3s3I3Bs9f3Bs8f5I19f3Bs3Bs3Bs11f',size,readId)
            elif size == 224:
                unpacked = ins.unpack('B3s3I3Bs9f3Bs8f5I19f3Bs3Bs3Bs6f',size,readId)
            else:
                raise "Unexpected size encountered for EFSH subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, record.flags.getTrueAttrs()
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('ICON','fillTexture'),
        MelString('ICO2','particleTexture'),
        MelString('NAM7','holesTexture'),
        MelEfshData('DATA','B3s3I3Bs9f3Bs8f5I19f3Bs3Bs3Bs11fI5f3Bsf2I6f',
            (_flags,'flags'),('unused1',null3),'memSBlend',
            'memBlendOp','memZFunc','fillRed','fillGreen','fillBlue',
            ('unused2',null1),'fillAIn','fillAFull','fillAOut','fillAPRatio',
            'fillAAmp','fillAFreq','fillAnimSpdU','fillAnimSpdV','edgeOff',
            'edgeRed','edgeGreen','edgeBlue',('unused3',null1),'edgeAIn',
            'edgeAFull','edgeAOut','edgeAPRatio','edgeAAmp','edgeAFreq',
            'fillAFRatio','edgeAFRatio','memDBlend',('partSBlend',5),
            ('partBlendOp',1),('partZFunc',4),('partDBlend',6),('partBUp',0.0),
            ('partBFull',0.0),('partBDown',0.0),('partBFRatio',1.0),
            ('partBPRatio',1.0),('partLTime',1.0),('partLDelta',0.0),
            ('partNSpd',0.0),('partNAcc',0.0),('partVel1',0.0),('partVel2',0.0),
            ('partVel3',0.0),('partAcc1',0.0),('partAcc2',0.0),('partAcc3',0.0),
            ('partKey1',1.0),('partKey2',1.0),('partKey1Time',0.0),
            ('partKey2Time',1.0),('key1Red',255),('key1Green',255),
            ('key1Blue',255),('unused4',null1),('key2Red',255),('key2Green',255),
            ('key2Blue',255),('unused5',null1),('key3Red',255),('key3Green',255),
            ('key3Blue',255),('unused6',null1),('key1A',1.0),('key2A',1.0),
            ('key3A',1.0),('key1Time',0.0),('key2Time',0.5),('key3Time',1.0),
            ('partNSpdDelta',0.00000),('partRot',0.00000),
            ('partRotDelta',0.00000),('partRotSpeed',0.00000),
            ('partRotSpeedDelta',0.00000),(FID,'addonModels',None),
            ('holesStartTime',0.00000),('holesEndTime',0.00000),
            ('holesStartVal',0.00000),('holesEndVal',0.00000),
            ('edgeWidth',0.00000),('edgeRed',255),('edgeGreen',255),
            ('edgeBlue',255),('unused7',null1),('explosionWindSpeed',0.00000),
            ('textureCountU',1),('textureCountV',1),
            ('addonModelsFadeInTime',1.00000),('addonModelsFadeOutTime',1.00000),
            ('addonModelsScaleStart',1.00000),('addonModelsScaleEnd',1.00000),
            ('addonModelsScaleInTime',1.00000),('addonModelsScaleOutTime',1.00000),
            ),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreEnch(MelRecord,MreHasEffects):
    """Enchantment (Object Effect) record."""
    classType = 'ENCH'
    _flags = Flags(0L,Flags.getNames('noAutoCalc','autoCalculate','hideEffect'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelFull0(), #--At least one mod has this. Odd.
        MelStruct('ENIT','3IB3s','itemType','chargeAmount','enchantCost',
                 (_flags,'flags',0L),('unused1',null3)),
        #--itemType = 0: Scroll, 1: Staff, 2: Weapon, 3: Apparel
        MelEffects(),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreExpl(MelRecord):
    """Explosion record."""
    classType = 'EXPL'
    _flags = Flags(0,Flags.getNames(
        (1, 'alwaysUsesWorldOrientation'),
        (2, 'knockDownAlways'),
        (3, 'knockDownByFormular'),
        (4, 'ignoreLosCheck'),
        (5, 'pushExplosionSourceRefOnly'),
        (6, 'ignoreImageSpaceSwap'),
    ))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelFid('EITM','objectEffect'),
        MelFid('MNAM','imageSpaceModifier'),
        MelStruct('DATA','fffIIIfIIfffI','force','damage','radius',(FID,'light',None),
                  (FID,'sound1',None),(_flags,'flags'),'isRadius',(FID,'impactDataset',None),
                  (FID,'sound2',None),'radiationLevel','radiationTime','radiationRadius','soundLevel'),
        MelFid('INAM','placedImpactObject'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreEyes(MelRecord):
    """Eyes record."""
    classType = 'EYES'
    _flags = Flags(0L,Flags.getNames(
            (0, 'playable'),
            (1, 'notMale'),
            (2, 'notFemale'),
    ))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelString('ICON','iconPath'),
        MelStruct('DATA','B',(_flags,'flags')),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreFact(MelRecord):
    """Faction record."""
    classType = 'FACT'
    _flags = Flags(0L,Flags.getNames('hiddenFromPC','evil','specialCombat'))
    _flags2 = Flags(0L,Flags.getNames('trackCrime','allowSell',))

    class MelFactData(MelStruct):
        """Handle older truncated DATA for FACT subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 4:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 2:
                #--Else 2 byte record
                unpacked = ins.unpack('2B',size,readId)
            elif size == 1:
                #--Else 1 byte record
                unpacked = ins.unpack('B',size,readId)
            else:
                raise "Unexpected size encountered for FACT:DATA subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked

    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelStructs('XNAM','IiI','relations',(FID,'faction'),'mod','combatReaction'),
        MelFactData('DATA','2B2s',(_flags,'flags',0L),'flagsFact','unknown'),
        MelOptStruct('CNAM','f',('crimeGoldMultiplier',None)),
        MelGroups('ranks',
            MelStruct('RNAM','i','rank'),
            MelString('MNAM','male'),
            MelString('FNAM','female'),
            MelString('INAM','insigniaPath'),),
        MelOptStruct('WMI1','I',(FID,'reputation',None)),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreFlst(MelRecord):
    """FormID list record."""
    classType = 'FLST'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelFids('LNAM','formIDInList'),
        )
    __slots__ = (MelRecord.__slots__ + melSet.getSlotsUsed() +
        ['mergeOverLast','mergeSources','items','deflsts'])

    def __init__(self,header,ins=None,unpack=False):
        """Initialize."""
        MelRecord.__init__(self,header,ins,unpack)
        self.mergeOverLast = False #--Merge overrides last mod merged
        self.mergeSources = None #--Set to list by other functions
        self.items  = None #--Set of items included in list
        #--Set of items deleted by list (Deflst mods) unused for Skyrim
        self.deflsts = None

    def mergeFilter(self,modSet):
        """Filter out items that don't come from specified modSet."""
        if not self.longFids: raise StateError(_("Fids not in long format"))
        self.formIDInList = [fid for fid in self.formIDInList if fid[0] in modSet]

    def mergeWith(self,other,otherMod):
        """Merges newLevl settings and entries with self.
        Requires that: self.items, other.deflsts be defined."""
        if not self.longFids: raise StateError(_("Fids not in long format"))
        if not other.longFids: raise StateError(_("Fids not in long format"))
        #--Remove items based on other.removes
        if other.deflsts:
            removeItems = self.items & other.deflsts
            self.formIDInList = [fid for fid in self.formIDInList if fid not in removeItems]
            self.items = (self.items | other.deflsts)
        hasOldItems = bool(self.items)
        #--Add new items from other
        newItems = set()
        formIDInListAppend = self.formIDInList.append
        newItemsAdd = newItems.add
        for fid in other.formIDInList:
            if fid not in self.items:
                formIDInListAppend(fid)
                newItemsAdd(fid)
        if newItems:
            self.items |= newItems
            self.formIDInList.sort
        #--Is merged list different from other? (And thus written to patch.)
        if len(self.formIDInList) != len(other.formIDInList):
            self.mergeOverLast = True
        else:
            for selfEntry,otherEntry in zip(self.formIDInList,other.formIDInList):
                if selfEntry != otherEntry:
                    self.mergeOverLast = True
                    break
            else:
                self.mergeOverLast = False
        if self.mergeOverLast:
            self.mergeSources.append(otherMod)
        else:
            self.mergeSources = [otherMod]
        #--Done
        self.setChanged()

#------------------------------------------------------------------------------
class MreFurn(MelRecord):
    """Furniture record."""
    classType = 'FURN'
    _flags = Flags() #--Governs type of furniture and which anims are available
    #--E.g., whether it's a bed, and which of the bed entry/exit animations are available
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelStruct('MNAM','I',(_flags,'activeMarkers',0L)), ####ByteArray
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
# Marker for organization please don't remove ---------------------------------
# GLOB ------------------------------------------------------------------------
# Defined in brec.py as class MreGlob(MelRecord) ------------------------------
#------------------------------------------------------------------------------
class MreGmst(MreGmstBase):
    """Fallout New Vegas GMST record"""
    Master = u'FalloutNV'
    isKeyedByEid = True # NULL fids are acceptable.

#------------------------------------------------------------------------------
class MreGras(MelRecord):
    """Grass record."""
    classType = 'GRAS'
    _flags = Flags(0,Flags.getNames('vLighting','uScaling','fitSlope'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelModel(),
        MelStruct('DATA','3BsH2sI4fB3s','density','minSlope',
                  'maxSlope',('unused1',null1),'waterDistance',('unused2',null2),
                  'waterOp','posRange','heightRange','colorRange',
                  'wavePeriod',(_flags,'flags'),('unused3',null3)),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreHair(MelRecord):
    """Hair record."""
    classType = 'HAIR'
    _flags = Flags(0L,Flags.getNames('playable','notMale','notFemale','fixed'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelStruct('DATA','B',(_flags,'flags')),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreHdpt(MelRecord):
    """Head part record."""
    classType = 'HDPT'
    _flags = Flags(0L,Flags.getNames('playable',))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelModel(),
        MelStruct('DATA','B',(_flags,'flags')),
        MelFids('HNAM','extraParts'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreHung(MelRecord):
    """Hunger stage record."""
    classType = 'HUNG'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('DATA','2I','trigerThreshold',(FID,'actorEffect')),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreIdle(MelRecord):
    """Idle record."""
    classType = 'IDLE'
    #--Mel IDLE DATA
    class MelIdleData(MelStruct):
        """Handle older truncated DATA for IDLE subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 8:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 6:
                #--Else 6 byte record (skips flags and unknown2...
                unpacked = ins.unpack('3Bsh',size,readId)
            else:
                raise "Unexpected size encountered for IDLE:DATA subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, record.flags.getTrueAttrs()
    melSet = MelSet(
        MelString('EDID','eid'),
        MelModel(),
        MelConditions(),
        MelStruct('ANAM','II',(FID,'parent'),(FID,'prevId')),
        MelIdleData('DATA','3BshBs','group','loopMin','loopMax','unknown1',
                    'delay','flags','unknown2'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreIdlm(MelRecord):
    """Idle marker record."""
    classType = 'IDLM'
    _flags = Flags(0L,Flags.getNames('runInSequence',None,'doOnce'))
    class MelIdlmIdlc(MelStruct):
        """Handle older truncated IDLC for IDLM subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 4:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 1:
                unpacked = ins.unpack('B',size,readId)
            else:
                raise "Unexpected size encountered for IDLM:IDLC subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelStruct('IDLF','B',(_flags,'flags')),
        MelIdlmIdlc('IDLC','B3s','animationCount',('unused',null3)),
        MelStruct('IDLT','f','idleTimerSetting'),
        MelFidList('IDLA','animations'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreImad(MelRecord):
    """Image space modifier record."""
    classType = 'IMAD'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelBase('DNAM','dnam_p'),
        MelBase('BNAM','bnam_p'),
        MelBase('VNAM','vnam_p'),
        MelBase('TNAM','tnam_p'),
        MelBase('NAM3','nam3_p'),
        MelBase('RNAM','rnam_p'),
        MelBase('SNAM','snam_p'),
        MelBase('UNAM','unam_p'),
        MelBase('NAM1','nam1_p'),
        MelBase('NAM2','nam2_p'),
        MelBase('WNAM','wnam_p'),
        MelBase('XNAM','xnam_p'),
        MelBase('YNAM','ynam_p'),
        MelBase('NAM4','nam4_p'),
        MelBase('\x00IAD','_00IAD'),
        MelBase('\x40IAD','_atiad_p'),
        MelBase('\x01IAD','_01IAD'),
        MelBase('AIAD','aiad_p'),
        MelBase('\x02IAD','_02IAD'),
        MelBase('BIAD','biad_p'),
        MelBase('\x03IAD','_03IAD'),
        MelBase('CIAD','ciad_p'),
        MelBase('\x04IAD','_04IAD'),
        MelBase('DIAD','diad_p'),
        MelBase('\x05IAD','_05IAD'),
        MelBase('EIAD','eiad_p'),
        MelBase('\x06IAD','_06IAD'),
        MelBase('FIAD','fiad_p'),
        MelBase('\x07IAD','_07IAD'),
        MelBase('GIAD','giad_p'),
        MelBase('\x08IAD','_08IAD'),
        MelBase('HIAD','hiad_p'),
        MelBase('\x09IAD','_09IAD'),
        MelBase('IIAD','iiad_p'),
        MelBase('\x0aIAD','_0aIAD'),
        MelBase('JIAD','jiad_p'),
        MelBase('\x0bIAD','_0bIAD'),
        MelBase('KIAD','kiad_p'),
        MelBase('\x0cIAD','_0cIAD'),
        MelBase('LIAD','liad_p'),
        MelBase('\x0dIAD','_0dIAD'),
        MelBase('MIAD','miad_p'),
        MelBase('\x0eIAD','_0eIAD'),
        MelBase('NIAD','niad_p'),
        MelBase('\x0fIAD','_0fIAD'),
        MelBase('OIAD','oiad_p'),
        MelBase('\x10IAD','_10IAD'),
        MelBase('PIAD','piad_p'),
        MelBase('\x11IAD','_11IAD'),
        MelBase('QIAD','qiad_p'),
        MelBase('\x12IAD','_12IAD'),
        MelBase('RIAD','riad_p'),
        MelBase('\x13IAD','_13iad_p'),
        MelBase('SIAD','siad_p'),
        MelBase('\x14IAD','_14iad_p'),
        MelBase('TIAD','tiad_p'),
        MelFid('RDSD','soundIntro'),
        MelFid('RDSI','soundOutro'),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreImgs(MelRecord):
    """Imgs Item"""
    classType = 'IMGS'

    _flags = Flags(0L,Flags.getNames(
        'saturation',
        'contrast',
        'tint',
        'brightness'
    ))

    # Original Size 152 Bytes, FNVEdit says it can be 132 or 148 also
    class MelDnamData(MelStruct):
        """Handle older truncated DNAM for IMGS subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 152:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 148:
                unpacked = ins.unpack('33f4s4s4s4s',size,readId)
            elif size == 132:
                unpacked = ins.unpack('33f',size,readId)
            else:
                raise "Unexpected size encountered for IMGS:DNAM subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, record.flags.getTrueAttrs()

    melSet = MelSet(
        MelString('EDID','eid'),
        MelDnamData('DNAM','33f4s4s4s4sB3s','eyeAdaptSpeed','blurRadius','blurPasses',
                  'emissiveMult','targetLUM','upperLUMClamp','brightScale',
                  'brightClamp','lumRampNoTex','lumRampMin','lumRampMax',
                  'sunlightDimmer','grassDimmer','treeDimmer','skinDimmer',
                  'bloomBlurRadius','bloomAlphaMultInterior',
                  'bloomAlphaMultExterior','getHitBlurRadius',
                  'getHitBlurDampingConstant','getHitDampingConstant',
                  'nightEyeTintRed','nightEyeTintGreen','nightEyeTintBlue',
                  'nightEyeBrightness','cinematicSaturation',
                  'cinematicAvgLumValue','cinematicValue',
                  'cinematicBrightnessValue','cinematicTintRed',
                  'cinematicTintGreen','cinematicTintBlue','cinematicTintValue',
                  ('unused1',null4),('unused2',null4),('unused3',null4),('unused4',null4),
                  (_flags,'flags'),('unused5',null3)),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreImod(MelRecord):
    """Item mod."""
    classType = 'IMOD'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('SCRI','script'),
        MelString('DESC','description'),
        MelDestructible(),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        MelStruct('DATA','If','value','weight'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreInfo(MelRecord):
    """Info (dialog entry) record."""
    classType = 'INFO'
    _flags = Flags(0,Flags.getNames(
        'goodbye','random','sayOnce','runImmediately','infoRefusal','randomEnd',
        'runForRumors','speechChallenge',))
    _flags2 = Flags(0,Flags.getNames(
        'sayOnceADay','alwaysDarken',None,None,'lowIntelligence','highIntelligence',))
    _variableFlags = Flags(0L,Flags.getNames('isLongOrShort'))
    class MelInfoData(MelStruct):
        """Support older 2 byte version."""
        def loadData(self,record,ins,type,size,readId):
            if size != 2:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            unpacked = ins.unpack('2B',size,readId)
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print (record.dialType,record.flags.getTrueAttrs())

    class MelInfoSchr(MelStruct):
        """Print only if schd record is null."""
        def dumpData(self,record,out):
            if not record.schd_p:
                MelStruct.dumpData(self,record,out)
    #--MelSet
    melSet = MelSet(
        MelInfoData('DATA','HH','dialType','nextSpeaker',(_flags,'flags'),(_flags2,'flagsInfo'),),
        MelFid('QSTI','quests'),
        MelFid('TPIC','topic'),
        MelFid('PNAM','prevInfo'),
        MelFids('NAME','addTopics'),
        MelGroups('responses',
            MelStruct('TRDT','Ii4sB3sIB3s','emotionType','emotionValue',('unused1',null4),'responseNum',('unused2','0xcd0xcd0xcd'),
                      (FID,'sound'),'flags',('unused3','0xcd0xcd0xcd')),
            MelString('NAM1','responseText'),
            MelString('NAM2','actorNotes'),
            MelString('NAM3','edits'),
            MelFid('SNAM','speakerAnimation'),
            MelFid('LNAM','listenerAnimation'),
            ),
        MelConditions(),
        MelFids('TCLT','choices'),
        MelFids('TCLF','linksFrom'),
        MelFids('TCFU','tcfu_p'),
        # MelBase('SCHD','schd_p'), #--Old format script header?
        MelGroup('scriptBegin',
            MelInfoSchr('SCHR','4s4I',('unused2',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            ),
        MelGroup('scriptEnd',
            MelBase('NEXT','marker'),
            MelInfoSchr('SCHR','4s4I',('unused2',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            ),
        # MelFid('SNDD','sndd_p'),
        MelString('RNAM','prompt'),
        MelFid('ANAM','speaker'),
        MelFid('KNAM','acterValuePeak'),
        MelStruct('DNAM', 'I', 'speechChallenge')
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreIngr(MelRecord,MreHasEffects):
    """INGR (ingredient) record."""
    classType = 'INGR'
    _flags = Flags(0L,Flags.getNames('noAutoCalc','isFood'))
    # Equiptment Type
    # -1, None
    #  0, Big Guns',
    #  1, Energy Weapons',
    #  2, Small Guns',
    #  3, Melee Weapons',
    #  4, Unarmed Weapon',
    #  5, Thrown Weapons',
    #  6, Mine',
    #  7, Body Wear',
    #  8, Head Wear',
    #  9, Hand Wear',
    # 10, Chems',
    # 11, Stimpack',
    # 12, Food',
    # 13, Alcohol'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelFull0(),
        MelModel(),
        MelString('ICON','iconPath'),
        MelFid('SCRI','script'),
        #-1:None,0:Big Guns,1:Energy Weapons,2:Small Guns,3:Melee Weapons,
        #4:Unarmed Weapon,5:Thrown Weapons,6:Mine,7:Body Wear,8:Head Wear,
        #9:Hand Wear,10:Chems,11:Stimpack,12:Food,13:Alcohol
        MelStruct('ETYP','i',('etype',-1)),
        MelStruct('DATA','f','weight'),
        MelStruct('ENIT','iB3s','value',(_flags,'flags',0L),('unused1',null3)),
        MelEffects(),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreIpct(MelRecord):
    """Impact record."""
    classType = 'IPCT'

    DecalDataFlags = Flags(0L,Flags.getNames(
            (0, 'parallax'),
            (0, 'alphaBlending'),
            (0, 'alphaTesting'),
            (0, 'noSubtextures'),
        ))

    melSet = MelSet(
        MelString('EDID','eid'),
        MelModel(),
        MelStruct('DATA','fIffII','effectDuration','effectOrientation',
                  'angleThreshold','placementRadius','soundLevel','flags'),
        MelOptStruct('DODT','7fBB2s3Bs','minWidth','maxWidth','minHeight',
                     'maxHeight','depth','shininess','parallaxScale',
                     'parallaxPasses',(DecalDataFlags,'flags',0L),
                     ('unused1',null2),'red','green','blue',('unused2',null1)),
        MelFid('DNAM','textureSet'),
        MelFid('SNAM','sound1'),
        MelFid('NAM1','sound2'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreIpds(MelRecord):
    """Impact Dataset record."""
    classType = 'IPDS'
    class MelIpdsData(MelStruct):
        """Handle older truncated DATA for IPDS subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 48:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 40:
                unpacked = ins.unpack('10I',size,readId)
            elif size == 36:
                unpacked = ins.unpack('9I',size,readId)
            else:
                raise "Unexpected size encountered for IPDS:DATA subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked
    melSet = MelSet(
        MelString('EDID','eid'),
        MelIpdsData('DATA','12I',(FID,'stone',0),(FID,'dirt',0),
                    (FID,'grass',0),(FID,'glass',0),(FID,'metal',0),
                    (FID,'wood',0),(FID,'organic',0),(FID,'cloth',0),
                    (FID,'water',0),(FID,'hollowMetal',0),(FID,'organicBug',0),
                    (FID,'organicGlow',0)),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreKeym(MelRecord):
    """MISC (miscellaneous item) record."""
    classType = 'KEYM'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        MelStruct('DATA','if','value','weight'),
        MelFid('RNAM','soundRandomLooping'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreLgtm(MelRecord):
    """Lgtm Item"""
    classType = 'LGTM'

    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('DATA','3Bs3Bs3Bs2f2i3f',
            'redLigh','greenLigh','blueLigh','unknownLigh',
            'redDirect','greenDirect','blueDirect','unknownDirect',
            'redFog','greenFog','blueFog','unknownFog',
            'fogNear','fogFar',
            'dirRotXY','dirRotZ',
            'directionalFade','fogClipDist','fogPower',),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreLigh(MelRecord):
    """Light source record."""
    classType = 'LIGH'
    _flags = Flags(0L,Flags.getNames('dynamic','canTake','negative','flickers',
        'unk1','offByDefault','flickerSlow','pulse','pulseSlow','spotLight','spotShadow'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelModel(),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelString('FULL','full'),
        MelString('ICON','iconPath'),
        MelStruct('DATA','iI3BsI2fIf','duration','radius','red','green','blue',
                  ('unused1',null1),(_flags,'flags',0L),'falloff','fov','value',
                  'weight'),
        MelOptStruct('FNAM','f',('fade',None)),
        MelFid('SNAM','sound'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreLscr(MelRecord):
    """Load screen."""
    classType = 'LSCR'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('ICON','iconPath'),
        MelString('DESC','text'),
        MelStructs('LNAM','2I2h','Locations',(FID,'direct'),(FID,'indirect'),'gridy','gridx'),
        MelFid('WMI1','loadScreenType'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreLsct(MelRecord):
    """Load screen tip."""
    classType = 'LSCT'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('DATA','5IfI3fI20sI3f4sI','type','data1X','data1Y','data1Width',
                         'data1Height','data1Orientation',
            'data1Font','data1ColorR','data1ColorG','data1ColorB','data1Align','unknown1',
            'data2Font','data2ColorR','data2ColorG','data2ColorB','unknown2','stats'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreLtex(MelRecord):
    """Landscape Texture."""
    classType = 'LTEX'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('ICON','iconPath'),
        MelFid('TNAM', 'texture'),
        MelOptStruct('HNAM','3B','materialType','friction','restitution'),
        MelOptStruct('SNAM','B','specular'),
        MelFids('GNAM', 'grass'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreLvlc(MreLeveledList):
    """LVLC record. Leveled list for creatures."""
    classType = 'LVLC'
    __slots__ = MreLeveledList.__slots__

#------------------------------------------------------------------------------
class MreLvli(MreLeveledList):
    """LVLI record. Leveled list for items."""
    classType = 'LVLI'
    __slots__ = MreLeveledList.__slots__

#------------------------------------------------------------------------------
class MreLvln(MreLeveledList):
    """LVLN record. Leveled list for NPC."""
    classType = 'LVLN'
    __slots__ = MreLeveledList.__slots__

#------------------------------------------------------------------------------
class MreMesg(MelRecord):
    """Message Record."""
    classType = 'MESG'

    MesgTypeFlags = Flags(0L,Flags.getNames(
            (0, 'messageBox'),
            (1, 'autoDisplay'),
        ))

    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('DESC','description'),
        MelLString('FULL','full'),
        MelFid('INAM','icon'),
        MelBase('NAM0', 'unused_0'),
        MelBase('NAM1', 'unused_1'),
        MelBase('NAM2', 'unused_2'),
        MelBase('NAM3', 'unused_3'),
        MelBase('NAM4', 'unused_4'),
        MelBase('NAM5', 'unused_5'),
        MelBase('NAM6', 'unused_6'),
        MelBase('NAM7', 'unused_7'),
        MelBase('NAM8', 'unused_8'),
        MelBase('NAM9', 'unused_9'),
        MelStruct('DNAM','I',(MesgTypeFlags,'flags',0L),),
        MelStruct('TNAM','I','displayTime',),
        MelGroups('menuButtons',
            MelString('ITXT','buttonText'),
            MelConditions(),
            ),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreMgef(MelRecord):
    """MGEF (magic effect) record."""
    classType = 'MGEF'
    #--Main flags
    _flags = Flags(0L,Flags.getNames(
        ( 0,'hostile'),
        ( 1,'recover'),
        ( 2,'detrimental'),
        ( 3,'magnitude'),
        ( 4,'self'),
        ( 5,'touch'),
        ( 6,'target'),
        ( 7,'noDuration'),
        ( 8,'noMagnitude'),
        ( 9,'noArea'),
        (10,'fxPersist'),
        (11,'spellmaking'),
        (12,'enchanting'),
        (13,'noIngredient'),
        (16,'useWeapon'),
        (17,'useArmor'),
        (18,'useCreature'),
        (19,'useSkill'),
        (20,'useAttr'),
        (24,'useAV'),
        (25,'sprayType'),
        (26,'boltType'),
        (27,'noHitEffect'),))

    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelString('DESC','text'),
        MelString('ICON','iconPath'),
        MelModel(),
        MelStruct('DATA','IfI2iH2sIf6I2fIi',
            (_flags,'flags'),'baseCost',(FID,'associated'),'school','resistValue',
            'counterEffectCount',('unused1',null2),(FID,'light',0),'projectileSpeed',
            (FID,'effectShader',0),(FID,'objectDisplayShader',0),
            (FID,'castingSound',0),(FID,'boltSound',0),(FID,'hitSound',0),
            (FID,'areaSound',0),('cefEnchantment',0.0),('cefBarter',0.0),
            'archType','actorValue'),
        MelGroups('counterEffects',
            MelOptStruct('ESCE','I',(FID,'counterEffectCode',0)),),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

    def dumpData(self,out):
        counterEffects = self.counterEffects
        self.counterEffectCount = len(counterEffects) if counterEffects else 0
        MelRecord.dumpData(self,out)

#------------------------------------------------------------------------------
class MreMicn(MelRecord):
    """Menu icon record."""
    classType = 'MICN'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreMisc(MelRecord):
    """MISC (miscellaneous item) record."""
    classType = 'MISC'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        MelStruct('DATA','if','value','weight'),
        MelFid('RNAM','soundRandomLooping'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreMset(MelRecord):
    """Media Set."""
    classType = 'MSET'
    _flags = Flags(0L,Flags.getNames(
        ( 0,'dayOuter'),
        ( 1,'dayMiddle'),
        ( 2,'dayInner'),
        ( 3,'nightOuter'),
        ( 4,'nightMiddle'),
        ( 5,'nightInner'),
        ))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        #-1:'No Set',0:'Battle Set',1:'Location Set',2:'Dungeon Set',3:'Incidental Set'
        MelStruct('NAM1','I','type'),
        MelString('NAM2','nam2'),
        MelString('NAM3','nam3'),
        MelString('NAM4','nam4'),
        MelString('NAM5','nam5'),
        MelString('NAM6','nam6'),
        MelString('NAM7','nam7'),
        MelStruct('NAM8','f','nam8'),
        MelStruct('NAM9','f','nam9'),
        MelStruct('NAM0','f','nam0'),
        MelStruct('ANAM','f','anam'),
        MelStruct('BNAM','f','bnam'),
        MelStruct('CNAM','f','cnam'),
        MelStruct('JNAM','f','jnam'),
        MelStruct('KNAM','f','knam'),
        MelStruct('LNAM','f','lnam'),
        MelStruct('MNAM','f','mnam'),
        MelStruct('NNAM','f','nnam'),
        MelStruct('ONAM','f','onam'),
        MelStruct('PNAM','B',(_flags,'enableFlags'),),
        MelStruct('DNAM','f','dnam'),
        MelStruct('ENAM','f','enam'),
        MelStruct('FNAM','f','fnam'),
        MelStruct('GNAM','f','gnam'),
        MelOptStruct('HNAM','I',(FID,'hnam')),
        MelOptStruct('INAM','I',(FID,'inam')),
        MelBase('DATA','data'),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreMstt(MelRecord):
    """Moveable static record."""
    classType = 'MSTT'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelDestructible(),
        MelBase('DATA','data_p'),
        MelFid('SNAM','sound'),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreMusc(MelRecord):
    """Music type record."""
    classType = 'MUSC'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FNAM','filename'),
        MelStruct('ANAM','f','dB'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreNavi(MelRecord):
    """Navigation Mesh Info Map."""
    classType = 'NAVI'
    class MelNaviNvmi(MelStructs):
        """Handle older truncated NVMI for NAVI subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size <= 16:
                raise "Unexpected size encountered for NAVI subrecord: %s" % size
            format = '4s2I2H %ds'%(size-16)
            target = self.getDefault()
            record.__getattribute__(self.attr).append(target)
            target.__slots__ = self.attrs
            unpacked = ins.unpack(format,size,readId)
            setter = target.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, target.flags.getTrueAttrs()
        def dumpData(self,record,out):
            """Dumps data from record to outstream."""
            for target in record.__getattribute__(self.attr):
                format = '4s2I2H %ds'%len(target.unknown2)
                values = []
                valuesAppend = values.append
                getter = target.__getattribute__
                for attr,action in zip(self.attrs,self.actions):
                    value = getter(attr)
                    if action: value = value.dump()
                    valuesAppend(value)
                try:
                    out.packSub(self.subType,format,*values)
                except struct.error:
                    print self.subType,format,values
                    raise
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('NVER','I',('version',11)),
        MelNaviNvmi('NVMI','','unknowns',
                   'unknown1',(FID,'navigationMesh'),(FID,'location'),'gridX','gridY','unknown2'),
        MelFidList('NVCI','unknownDoors',),
       )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreNavm(MelRecord):
    """Navigation Mesh."""
    classType = 'NAVM'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('NVER','I',('version',11)),
        MelStruct('DATA','I5I',(FID,'cell'),'vertexCount','triangleCount','enternalConnectionsCount','nvcaCount','doorsCount'),
        MelStructA('NVVX','3f','vertices','vertexX','vertexY','vertexZ'),
        MelStructA('NVTR','6hI','triangles','vertex0','vertex1','vertex2','triangle0','triangle1','triangle2','flags'),
        MelOptStruct('NVCA','h','nvca_p'),
        MelStructA('NVDP','II','doors',(FID,'doorReference'),'doorUnknown'),
        MelBase('NVGD','nvgd_p'),
        MelStructA('NVEX','=IIH','externalConnections','nvexUnknown',(FID,'navigationMesh'),'triangle'),
       )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreNote(MelRecord):
    """Note record."""
    classType = 'NOTE'
    class MelNoteTnam(MelBase):
        """text or topic"""
        def hasFids(self,formElements):
            formElements.add(self)
        def loadData(self,record,ins,type,size,readId):
            #0:'sound',1:'text',2:'image',3:'voice'
            if record.dataType == 1: # text (string)
                value = ins.readString(size,readId)
                record.__setattr__(self.attr, (False, value))
            elif record.dataType == 3: # voice (fid:DIAL)
                (value,) = ins.unpack('I',size,readId)
                record.__setattr__(self.attr, (True, value))
            else:
                raise ModError(ins.inName,_('Unexpected type: %d') % record.type)
            if self._debug: print unpacked
        def dumpData(self,record,out):
            value = record.__getattribute__(self.attr)
            if value is None: return
            (isFid, value) = value
            if value is not None:
                #0:'sound',1:'text',2:'image',3:'voice'
                if record.dataType == 1: # text (string)
                    out.packSub0(self.subType,value)
                elif record.dataType == 3: # voice (fid:DIAL)
                    out.packRef(self.subType,value)
                else:
                    raise ModError(ins.inName,_('Unexpected type: %d') % record.type)
        def mapFids(self,record,function,save=False):
            value = record.__getattribute__(self.attr)
            if value is None: return
            (isFid, value) = value
            if isFid:
                result = function(value)
                if save: record.__setattr__(self.attr,(isFid,result))
    class MelNoteSnam(MelBase):
        """sound or npc"""
        def hasFids(self,formElements):
            formElements.add(self)
        def loadData(self,record,ins,type,size,readId):
            #0:'sound',1:'text',2:'image',3:'voice'
            if record.dataType == 0: # sound (fid:SOUN)
                (value,) = ins.unpack('I',size,readId)
                record.__setattr__(self.attr, (True, value))
            elif record.dataType == 3: # voice (fid:NPC_)
                (value,) = ins.unpack('I',size,readId)
                record.__setattr__(self.attr, (True, value))
            else:
                raise ModError(ins.inName,_('Unexpected type: %d') % record.type)
            if self._debug: print unpacked
        def dumpData(self,record,out):
            value = record.__getattribute__(self.attr)
            if value is None: return
            (isFid, value) = value
            if value is not None: out.packRef(self.subType,value)
        def mapFids(self,record,function,save=False):
            value = record.__getattribute__(self.attr)
            if value is None: return
            (isFid, value) = value
            if isFid:
                result = function(value)
                if save: record.__setattr__(self.attr,(isFid,result))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        #0:'sound',1:'text',2:'image',3:'voice'
        MelStruct('DATA','B','dataType'),
        MelFidList('ONAM','quests'),
        MelString('XNAM','texture'),
        MelNoteTnam('TNAM', 'textTopic'),
        MelNoteSnam('SNAM', 'soundNpc'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreNpc(MreActor):
    """NPC Record. Non-Player Character."""
    classType = 'NPC_'
    #--Main flags
    _flags = Flags(0L,Flags.getNames(
        ( 0,'female'),
        ( 1,'essential'),
        ( 2,'isChargenFacePreset'),
        ( 3,'respawn'),
        ( 4,'autoCalc'),
        ( 7,'pcLevelOffset'),
        ( 8,'useTemplate'),
        ( 9,'noLowLevel'),
        (11,'noBloodSpray'),
        (12,'noBloodDecal'),
        (20,'noVATSMelee'),
        (22,'canBeAllRaces'),
        (23,'autocalcService'),
        (26,'noKnockDown'),
        (27,'notPushable'),
        (30,'noRotatingHeadTrack'),))
    #--AI Service flags
    aiService = Flags(0L,Flags.getNames(
        (0,'weapons'),
        (1,'armor'),
        (2,'clothing'),
        (3,'books'),
        (4,'foods'),
        (5,'chems'),
        (6,'stimpacks'),
        (7,'lights'),
        (10,'miscItems'),
        (13,'potions'),
        (14,'training'),
        (16,'recharge'),
        (17,'repair'),))
    aggroflags = Flags(0L,Flags.getNames('aggroRadiusBehavior',))
    #--Mel NPC DATA
    class MelNpcData(MelStruct):
        """Convert npc stats into skills, health, attributes."""
        def loadData(self,record,ins,type,size,readId):
            if size == 11:
                unpacked = list(ins.unpack('=I7B',size,readId))
            else:
                unpacked = list(ins.unpack('=I21B',size,readId))
            recordSetAttr = record.__setattr__
            recordSetAttr('health',unpacked[0])
            recordSetAttr('attributes',unpacked[1:])
            if self._debug: print unpacked[0],unpacked[1:]
        def dumpData(self,record,out):
            """Dumps data from record to outstream."""
            recordGetAttr = record.__getattribute__
            values = [recordGetAttr('health')]+recordGetAttr('attributes')
            if len(recordGetAttr('attributes')) == 7:
                out.packSub(self.subType,'=I7B',*values)
            else:
                out.packSub(self.subType,'=I21B',*values)

    #--Mel NPC DNAM
    class MelNpcDnam(MelStruct):
        """Convert npc stats into skills."""
        def loadData(self,record,ins,type,size,readId):
            unpacked = list(ins.unpack('=28B',size,readId))
            recordSetAttr = record.__setattr__
            recordSetAttr('skillValues',unpacked[:14])
            recordSetAttr('skillOffsets',unpacked[14:])
            if self._debug: print unpacked[:14]+unpacked[14:]
        def dumpData(self,record,out):
            """Dumps data from record to outstream."""
            recordGetAttr = record.__getattribute__
            values = recordGetAttr('skillValues')+recordGetAttr('skillOffsets')
            out.packSub(self.subType,'=28B',*values)

    #--Mel Set
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelStruct('ACBS','=I2Hh3Hf2H',(_flags,'flags',0L),'fatigue','barterGold',
                 ('level',1),'calcMin','calcMax','speedMultiplier','karma',
                 'dispotionBase','templateFlags'),
        MelStructs('SNAM','=IB3s','factions',(FID,'faction',None),'rank',('unused1','ODB')),
        MelFid('INAM','deathItem'),
        MelFid('VTCK','voice'),
        MelFid('TPLT','template'),
        MelFid('RNAM','race'),
        #MelFid('????','actorEffects'),
        MelFid('EITM','unarmedAttackEffect'),
        MelStruct('EAMT','H', 'unarmedAttackAnimation'),
        MelDestructible(),
        MelFids('SPLO','spells'),
        MelFid('SCRI','script'),
        MelGroups('items',
            MelStruct('CNTO','Ii',(FID,'item',None),('count',1)),
            MelOptStruct('COED','IIf',(FID,'owner',None),(FID,'glob',None),('condition',1.0)),
        ),
        MelStruct('AIDT','=5B3sIbBbBi',
        #0:Unaggressive,1:Aggressive,2:Very Aggressive,3:Frenzied
        ('aggression',0),
        #0:Cowardly,1:Cautious,2:Average,3:Brave,4:Foolhardy
        ('confidence',2),
        ('energyLevel',50),('responsibility',50),
        #0:Neutral,1:Afraid,2:Annoyed,3:Cocky,4:Drugged,5:Pleasant,6:Angry,7:Sad
        ('mood',0),
        ('unused_aidt',null3),(aiService,'services',0L),
        #-1:None,0:Barter,1:Big Guns (obsolete),2:Energy Weapons,3:Explosives
        #4:Lockpick,5:Medicine,6:Melee Weapons,7:Repair,8:Science,9:Guns,10:Sneak
        #11:Speech,12:Survival,13:Unarmed,
        ('trainSkill',-1),
        'trainLevel',
        #0:Helps Nobody,1:Helps Allies,2:Helps Friends and Allies
        ('assistance',0),
        (aggroflags,'aggroRadiusBehavior',0L),'aggroRadius'),
        MelFids('PKID','aiPackages'),
        MelStrings('KFFZ','animations'),
        MelFid('CNAM','iclass'),
        MelNpcData('DATA','','health',('attributes',[0]*21)),
        MelFids('PNAM','headParts'),
        MelNpcDnam('DNAM','',('skillValues',[0]*14),('skillOffsets',[0]*14)),
        MelFid('HNAM','hair'),
        MelOptStruct('LNAM','f',('hairLength',1)),
        MelFid('ENAM','eye'), ####fid Array
        MelStruct('HCLR','3Bs','hairRed','hairBlue','hairGreen',('unused3',null1)),
        MelFid('ZNAM','combatStyle'),
        MelStruct('NAM4','I',('impactMaterialType',0L)),
        MelBase('FGGS','fggs_p'), ####FaceGen Geometry-Symmetric
        MelBase('FGGA','fgga_p'), ####FaceGen Geometry-Asymmetric
        MelBase('FGTS','fgts_p'), ####FaceGen Texture-Symmetric
        MelStruct('NAM5','H',('unknown',0L)),
        MelStruct('NAM6','f',('height',0L)),
        MelStruct('NAM7','f',('weight',0L)),
        )
    __slots__ = MreActor.__slots__ + melSet.getSlotsUsed()

    def setRace(self,race):
        """Set additional race info."""
        self.race = race
        #--Model
        if not self.model:
            self.model = self.getDefault('model')
        if race in (0x23fe9,0x223c7):
            self.model.modPath = r"Characters\_Male\SkeletonBeast.NIF"
        else:
            self.model.modPath = r"Characters\_Male\skeleton.nif"
        #--FNAM
        # Needs Updating for Fallout New Vegas
        # American
        fnams = {
            0x23fe9 : 0x3cdc ,#--Argonian
            0x224fc : 0x1d48 ,#--Breton
            0x191c1 : 0x5472 ,#--Dark Elf
            0x19204 : 0x21e6 ,#--High Elf
            0x00907 : 0x358e ,#--Imperial
            0x22c37 : 0x5b54 ,#--Khajiit
            0x224fd : 0x03b6 ,#--Nord
            0x191c0 : 0x0974 ,#--Orc
            0x00d43 : 0x61a9 ,#--Redguard
            0x00019 : 0x4477 ,#--Vampire
            0x223c8 : 0x4a2e ,#--Wood Elf
            }
        self.fnam = fnams.get(race,0x358e)

#------------------------------------------------------------------------------
class MrePack(MelRecord):
    """AI package record."""
    classType = 'PACK'
    _flags = Flags(0,Flags.getNames(
        'offersServices','mustReachLocation','mustComplete','lockAtStart',
        'lockAtEnd','lockAtLocation','unlockAtStart','unlockAtEnd',
        'unlockAtLocation','continueIfPcNear','oncePerDay',None,
        'skipFallout','alwaysRun',None,None,
        None,'alwaysSneak','allowSwimming','allowFalls',
        'unequipArmor','unequipWeapons','defensiveCombat','useHorse',
        'noIdleAnims',))
    _variableFlags = Flags(0L,Flags.getNames('isLongOrShort'))
    class MelPackPkdt(MelStruct):
        """Support older 8 byte version."""
        def loadData(self,record,ins,type,size,readId):
            if size == 12:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 8:
                unpacked = ins.unpack('IHH',size,readId)
            else:
                raise "Unexpected size encountered for PACK:PKDT subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked
    class MelPackPkdd(MelOptStruct):
        """Handle older truncated PKDD for PACK subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 24:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 20:
                unpacked = ins.unpack('fII4sI',size,readId)
            elif size == 16:
                unpacked = ins.unpack('fII4s',size,readId)
            elif size == 12:
                unpacked = ins.unpack('fII',size,readId)
            else:
                raise "Unexpected size encountered for PACK:PKDD subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked
    class MelPackLT(MelOptStruct):
        """For PLDT and PTDT. Second element of both may be either an FID or a long,
        depending on value of first element."""
        def loadData(self,record,ins,type,size,readId):
            if ((self.subType == 'PLDT' and size == 12) or
                (self.subType == 'PLD2' and size == 12) or
                (self.subType == 'PTDT' and size == 16) or
                (self.subType == 'PTD2' and size == 16)):
                MelOptStruct.loadData(self,record,ins,type,size,readId)
                return
            elif ((self.subType == 'PTDT' and size == 12) or
                  (self.subType == 'PTD2' and size == 12)):
                unpacked = ins.unpack('iIi',size,readId)
            else:
                raise "Unexpected size encountered for PACK:%s subrecord: %s" % (self.subType, size)
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked
        def hasFids(self,formElements):
            formElements.add(self)
        def dumpData(self,record,out):
            if ((self.subType == 'PLDT' and (record.locType or record.locId)) or
                (self.subType == 'PLD2' and (record.locType2 or record.locId2)) or
                (self.subType == 'PTDT' and (record.targetType or record.targetId)) or
                (self.subType == 'PTD2' and (record.targetType2 or record.targetId2))):
                MelStruct.dumpData(self,record,out)
        def mapFids(self,record,function,save=False):
            """Applies function to fids. If save is true, then fid is set
            to result of function."""
            if self.subType == 'PLDT' and record.locType != 5:
                result = function(record.locId)
                if save: record.locId = result
            elif self.subType == 'PLD2' and record.locType2 != 5:
                result = function(record.locId2)
                if save: record.locId2 = result
            elif self.subType == 'PTDT' and record.targetType != 2:
                result = function(record.targetId)
                if save: record.targetId = result
            elif self.subType == 'PTD2' and record.targetType2 != 2:
                result = function(record.targetId2)
                if save: record.targetId2 = result
    class MelPackDistributor(MelNull):
        """Handles embedded script records. Distributes load
        duties to other elements as needed."""
        def __init__(self):
            self._debug = False
        def getLoaders(self,loaders):
            """Self as loader for structure types."""
            for type in ('POBA','POEA','POCA'):
                loaders[type] = self
        def setMelSet(self,melSet):
            """Set parent melset. Need this so that can reassign loaders later."""
            self.melSet = melSet
            self.loaders = {}
            for element in melSet.elements:
                attr = element.__dict__.get('attr',None)
                if attr: self.loaders[attr] = element
        def loadData(self,record,ins,type,size,readId):
            if type == 'POBA':
                element = self.loaders['onBegin']
            elif type == 'POEA':
                element = self.loaders['onEnd']
            elif type == 'POCA':
                element = self.loaders['onChange']
            for subtype in ('INAM','SCHR','SCDA','SCTX','SLSD','SCVR','SCRV','SCRO','TNAM'):
                self.melSet.loaders[subtype] = element
            element.loadData(record,ins,type,size,readId)
    #--MelSet
    melSet = MelSet(
        MelString('EDID','eid'),
        MelPackPkdt('PKDT','IHHI',(_flags,'flags'),'aiType','falloutBehaviorFlags','typeSpecificFlags'),
        MelPackLT('PLDT','iIi','locType','locId','locRadius'),
        MelPackLT('PLD2','iIi','locType2','locId2','locRadius2'),
        MelStruct('PSDT','2bBbi','month','day','date','time','duration'),
        MelPackLT('PTDT','iIif','targetType','targetId','targetCount','targetUnknown1'),
        MelConditions(),
        MelGroup('idleAnimations',
            MelStruct('IDLF','B','animationFlags'),
            MelBase('IDLC','animationCount'), # byte or short
            MelStruct('IDLT','f','idleTimerSetting'),
            MelFidList('IDLA','animations'),
            MelBase('IDLB','idlb_p'),
            ),
        MelBase('PKED','eatMarker'),
        MelOptStruct('PKE2','I','escordDistance'),
        MelFid('CNAM','combatStyle'),
        MelOptStruct('PKFD','f','followStartLocationTrigerRadius'),
        MelBase('PKPT','patrolFlags'), # byte or short
        MelOptStruct('PKW3','IBB3Hff4s','weaponFlags','fireRate','fireCount','numBursts',
                     'shootPerVolleysMin','shootPerVolleysMax','pauseBetweenVolleysMin','pauseBetweenVolleysMax','weaponUnknown'),
        MelPackLT('PTD2','iIif','targetType2','targetId2','targetCount2','targetUnknown2'),
        MelBase('PUID','useItemMarker'),
        MelBase('PKAM','ambushMarker'),
        MelPackPkdd('PKDD','fII4sI4s','dialFov','dialTopic','dialFlags','dialUnknown1','dialType','dialUnknown2'),
        MelGroup('onBegin',
            MelBase('POBA', 'marker', ''), #### onBegin Marker, wbEmpty
            MelFid('INAM', 'idle'),
            MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            MelFid('TNAM', 'topic'),
            ),
        MelGroup('onEnd',
            MelBase('POEA', 'marker', ''), #### onEnd Marker, wbEmpty
            MelFid('INAM', 'idle'),
            MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            MelFid('TNAM', 'topic'),
            ),
        MelGroup('onChange',
            MelBase('POCA', 'marker', ''), #### onChange Marker, wbEmpty
            MelFid('INAM', 'idle'),
            MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            MelFid('TNAM', 'topic'),
            ),
        #--Distributor for embedded script entries.
        MelPackDistributor(),
        )
    melSet.elements[-1].setMelSet(melSet)
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MrePerk(MelRecord):
    """Perk record."""
    classType = 'PERK'
    class MelPerkData(MelStruct):
        """Handle older truncated DATA for PERK subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 5:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 4:
                unpacked = ins.unpack('BBBB',size,readId)
            else:
                raise "Unexpected size encountered for DATA subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked, record.flagsA.getTrueAttrs()
    class MelPerkEffectData(MelBase):
        def hasFids(self,formElements):
            formElements.add(self)
        def loadData(self,record,ins,type,size,readId):
            target = MelObject()
            record.__setattr__(self.attr,target)
            if record.type == 0:
                format,attrs = ('II',('quest','queststage'))
            elif record.type == 1:
                format,attrs = ('I',('ability',))
            elif record.type == 2:
                format,attrs = ('HB',('entrypoint','function'))
            else:
                raise ModError(ins.inName,_('Unexpected type: %d') % record.type)
            unpacked = ins.unpack(format,size,readId)
            setter = target.__setattr__
            for attr,value in zip(attrs,unpacked):
                setter(attr,value)
            if self._debug: print unpacked
        def dumpData(self,record,out):
            target = record.__getattribute__(self.attr)
            if not target: return
            if record.type == 0:
                format,attrs = ('II',('quest','queststage'))
            elif record.type == 1:
                format,attrs = ('I',('ability',))
            elif record.type == 2:
                format,attrs = ('HB',('entrypoint','function'))
            else:
                raise ModError(ins.inName,_('Unexpected type: %d') % record.type)
            values = []
            valuesAppend = values.append
            getter = target.__getattribute__
            for attr in attrs:
                value = getter(attr)
                valuesAppend(value)
            try:
                out.packSub(self.subType,format,*values)
            except struct.error:
                print self.subType,format,values
                raise
        def mapFids(self,record,function,save=False):
            target = record.__getattribute__(self.attr)
            if not target: return
            if record.type == 0:
                result = function(target.quest)
                if save: target.quest = result
            elif record.type == 1:
                result = function(target.ability)
                if save: target.ability = result
    class MelPerkEffects(MelGroups):
        def __init__(self,attr,*elements):
            MelGroups.__init__(self,attr,*elements)
        def setMelSet(self,melSet):
            self.melSet = melSet
            self.attrLoaders = {}
            for element in melSet.elements:
                attr = element.__dict__.get('attr',None)
                if attr: self.attrLoaders[attr] = element
        def loadData(self,record,ins,type,size,readId):
            if type == 'DATA' or type == 'CTDA':
                effects = record.__getattribute__(self.attr)
                if not effects:
                    if type == 'DATA':
                        element = self.attrLoaders['_data']
                    elif type == 'CTDA':
                        element = self.attrLoaders['conditions']
                    element.loadData(record,ins,type,size,readId)
                    return
            MelGroups.loadData(self,record,ins,type,size,readId)
    class MelPerkEffectParams(MelGroups):
        def loadData(self,record,ins,type,size,readId):
            if type in ('EPFD','EPFT','EPF2','EPF3','SCHR'):
                target = self.getDefault()
                record.__getattribute__(self.attr).append(target)
            else:
                target = record.__getattribute__(self.attr)[-1]
            element = self.loaders[type]
            slots = ['recordType']
            slots.extend(element.getSlotsUsed())
            target.__slots__ = slots
            target.recordType = type
            element.loadData(target,ins,type,size,readId)
        def dumpData(self,record,out):
            for target in record.__getattribute__(self.attr):
                element = self.loaders[target.recordType]
                if not element:
                    raise ModError(ins.inName,_('Unexpected type: %d') % target.recordType)
                element.dumpData(target,out)

    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelString('DESC','description'),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelConditions(),
        MelGroup('_data',
            MelPerkData('DATA', 'BBBBB', ('trait',0), ('minLevel',0), ('ranks',0), ('playable',0), ('hidden',0)),
            ),
        MelPerkEffects('effects',
            MelStruct('PRKE', 'BBB', 'type', 'rank', 'priority'),
            MelPerkEffectData('DATA','effectData'),
            MelGroups('effectConditions',
                MelStruct('PRKC', 'B', 'runOn'),
                MelConditions(),
            ),
            MelPerkEffectParams('effectParams',
                MelBase('EPFD', 'floats'), # [Float] or [Float,Float], todo rewrite specific class
                MelStruct('EPFT','B','_epft'),
                MelString('EPF2','buttonLabel'),
                MelStruct('EPF3','H','scriptFlag'),
                MelGroup('embeddedScript',
                    MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
                    MelBase('SCDA','compiled_p'),
                    MelString('SCTX','scriptText'),
                    MelScrxen('SCRV/SCRO','references'),
                ),
            ),
            MelBase('PRKF','footer'),
            ),
        )
    melSet.elements[-1].setMelSet(melSet)
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MrePgre(MelRecord):
    """Placed Grenade"""
    classType = 'PGRE'
    _flags = Flags(0L,Flags.getNames('oppositeParent'))
    _variableFlags = Flags(0L,Flags.getNames('isLongOrShort'))
    _watertypeFlags = Flags(0L,Flags.getNames('reflection','refraction'))
    melSet=MelSet(
        MelString('EDID','eid'),
        MelFid('NAME','base'),
        MelFid('XEZN','encounterZone'),
        MelBase('XRGD','ragdollData'),
        MelBase('XRGB','ragdollBipedData'),
        MelGroup('patrolData',
            MelStruct('XPRD','f','idleTime'),
            MelBase('XPPA','patrolScriptMarker'),
            MelFid('INAM', 'idle'),
            MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            MelFid('TNAM','topic'),
            ),
        MelOwnership(),
        MelStruct('XCNT','i','count'),
        MelStruct('XRDS','f','radius',),
        MelStruct('XHLP','f','health',),
        MelGroups('reflectedRefractedBy',
            MelStruct('XPWR','2I',(FID,'waterReference'),(_watertypeFlags,'waterFlags',0L),),
        ),
        MelStructs('XDCR','II','linkedDecals',(FID,'reference'),'unknown'),
        MelFid('XLKR','linkedReference'),
        MelOptStruct('XCLP','8B','linkStartColorRed','linkStartColorGreen','linkStartColorBlue',('linkColorUnused1',null1),
                     'linkEndColorRed','linkEndColorGreen','linkEndColorBlue',('linkColorUnused2',null1)),
        MelGroup('activateParents',
            MelStruct('XAPD','B','flags'),
            MelStructs('XAPR','If','activateParentRefs',(FID,'reference'),'delay')
            ),
        MelString('XATO','activationPrompt'),
        MelOptStruct('XESP','IB3s',(FID,'parent'),(_flags,'parentFlags'),('unused1',null3)),
        MelOptStruct('XEMI','I',(FID,'emittance')),
        MelFid('XMBR','multiboundReference'),
        MelBase('XIBS','ignoredBySandbox'),
        MelOptStruct('XSCL','f',('scale',1.0)),
        MelOptStruct('DATA','=6f',('posX',None),('posY',None),('posZ',None),('rotX',None),('rotY',None),('rotZ',None)),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MrePmis(MelRecord):
    """Placed Missile"""
    classType = 'PMIS'
    _flags = Flags(0L,Flags.getNames('oppositeParent'))
    _variableFlags = Flags(0L,Flags.getNames('isLongOrShort'))
    _watertypeFlags = Flags(0L,Flags.getNames('reflection','refraction'))
    melSet=MelSet(
        MelString('EDID','eid'),
        MelFid('NAME','base'),
        MelFid('XEZN','encounterZone'),
        MelBase('XRGD','ragdollData'),
        MelBase('XRGB','ragdollBipedData'),
        MelGroup('patrolData',
            MelStruct('XPRD','f','idleTime'),
            MelBase('XPPA','patrolScriptMarker'),
            MelFid('INAM', 'idle'),
            MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            MelFid('TNAM','topic'),
            ),
        MelOwnership(),
        MelStruct('XCNT','i','count'),
        MelStruct('XRDS','f','radius',),
        MelStruct('XHLP','f','health',),
        MelGroups('reflectedRefractedBy',
            MelStruct('XPWR','2I',(FID,'waterReference'),(_watertypeFlags,'waterFlags',0L),),
        ),
        MelStructs('XDCR','II','linkedDecals',(FID,'reference'),'unknown'),
        MelFid('XLKR','linkedReference'),
        MelOptStruct('XCLP','8B','linkStartColorRed','linkStartColorGreen','linkStartColorBlue',('linkColorUnused1',null1),
                     'linkEndColorRed','linkEndColorGreen','linkEndColorBlue',('linkColorUnused2',null1)),
        MelGroup('activateParents',
            MelStruct('XAPD','B','flags'),
            MelStructs('XAPR','If','activateParentRefs',(FID,'reference'),'delay')
            ),
        MelString('XATO','activationPrompt'),
        MelOptStruct('XESP','IB3s',(FID,'parent'),(_flags,'parentFlags'),('unused1',null3)),
        MelOptStruct('XEMI','I',(FID,'emittance')),
        MelFid('XMBR','multiboundReference'),
        MelBase('XIBS','ignoredBySandbox'),
        MelOptStruct('XSCL','f',('scale',1.0)),
        MelOptStruct('DATA','=6f',('posX',None),('posY',None),('posZ',None),('rotX',None),('rotY',None),('rotZ',None)),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreProj(MelRecord):
    """Projectile record."""
    classType = 'PROJ'
    _flags = Flags(0,Flags.getNames(
        'hitscan',
        'explosive',
        'altTriger',
        'muzzleFlash',
        None,
        'canbeDisable',
        'canbePickedUp',
        'superSonic',
        'pinsLimbs',
        'passThroughSmallTransparent'
        'detonates',
        'rotation'
        ))
    class MelProjData(MelStruct):
        """Handle older truncated DATA for PROJ subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 84:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 68:
                unpacked = ins.unpack('HHfffIIfffIIfffIII',size,readId)
            else:
                raise "Unexpected size encountered for PROJ:DATA subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelDestructible(),
        MelProjData('DATA','HHfffIIfffIIfffIIIffff',(_flags,'flags'),'type',
                  ('gravity',0.00000),('speed',10000.00000),('range',10000.00000),
                  (FID,'light',0),(FID,'muzzleFlash',0),('tracerChance',0.00000),
                  ('explosionAltTrigerProximity',0.00000),('explosionAltTrigerTimer',0.00000),
                  (FID,'explosion',0),(FID,'sound',0),('muzzleFlashDuration',0.00000),
                  ('fadeDuration',0.00000),('impactForce',0.00000),
                  (FID,'soundCountDown',0),(FID,'soundDisable',0),
                  (FID,'defaultWeaponSource',0),('rotationX',0.00000),
                  ('rotationY',0.00000),('rotationZ',0.00000),('bouncyMult',0.00000)),
        MelString('NAM1','muzzleFlashPath'),
        MelBase('NAM2','_nam2'),
        MelStruct('VNAM','I','soundLevel'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MrePwat(MelRecord):
    """Placeable water record."""
    classType = 'PWAT'
    _flags = Flags(0L,Flags.getNames(
        ( 0,'reflects'),
        ( 1,'reflectsActers'),
        ( 2,'reflectsLand'),
        ( 3,'reflectsLODLand'),
        ( 4,'reflectsLODBuildings'),
        ( 5,'reflectsTrees'),
        ( 6,'reflectsSky'),
        ( 7,'reflectsDynamicObjects'),
        ( 8,'reflectsDeadBodies'),
        ( 9,'refracts'),
        (10,'refractsActors'),
        (11,'refractsLands'),
        (16,'refractsDynamicObjects'),
        (17,'refractsDeadBodies'),
        (18,'silhouetteReflections'),
        (28,'depth'),
        (29,'objectTextureCoordinates'),
        (31,'noUnderwaterFog'),
        ))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelModel(),
        MelStruct('DNAM','2I',(_flags,'flags'),(FID,'water'))
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreQust(MelRecord):
    """Quest record."""
    classType = 'QUST'
    _questFlags = Flags(0,Flags.getNames('startGameEnabled',None,'repeatedTopics','repeatedStages'))
    _variableFlags = Flags(0L,Flags.getNames('isLongOrShort'))
    stageFlags = Flags(0,Flags.getNames('complete'))
    targetFlags = Flags(0,Flags.getNames('ignoresLocks'))

    #--CDTA loader
    class MelQustLoaders(DataDict):
        """Since CDTA subrecords occur in three different places, we need
        to replace ordinary 'loaders' dictionary with a 'dictionary' that will
        return the correct element to handle the CDTA subrecord. 'Correct'
        element is determined by which other subrecords have been encountered."""
        def __init__(self,loaders,quest,stages,targets):
            self.data = loaders
            self.type_ctda = {'EDID':quest, 'INDX':stages, 'QSTA':targets}
            self.ctda = quest #--Which ctda element loader to use next.
        def __getitem__(self,key):
            if key == 'CTDA': return self.ctda
            self.ctda = self.type_ctda.get(key, self.ctda)
            return self.data[key]

    class MelQustData(MelStruct):
        """Handle older truncated DATA for QUST subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 8:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 2:
                #--Else 2 byte record
                unpacked = ins.unpack('BB',size,readId)
            else:
                raise "Unexpected size encountered for QUST:DATA subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked

    #--MelSet
    melSet = MelSet(
        MelString('EDID','eid'),
        MelFid('SCRI','script'),
        MelString('FULL','full'),
        MelString('ICON','iconPath'),
        MelQustData('DATA','=BB2sf',(_questFlags,'questFlags',0),('priority',0),('unused2',null2),('questDelay',0.0)),
        MelConditions(),
        MelGroups('stages',
            MelStruct('INDX','h','stage'),
            MelGroups('entries',
                MelStruct('QSDT','B',(stageFlags,'flags')),
                MelConditions(),
                MelString('CNAM','text'),
                MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
                MelBase('SCDA','compiled_p'),
                MelString('SCTX','scriptText'),
                MelGroups('vars',
                    MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                    MelString('SCVR','name')),
                MelScrxen('SCRV/SCRO','references'),
                MelFid('NAM0', 'nextQuest'),
                ),
            ),
        MelGroups('objectives',
             MelStruct('QOBJ','i','index'),
             MelString('NNAM','description'),
             MelGroups('targets',
                 MelStruct('QSTA','IB3s',(FID,'targetId'),(targetFlags,'flags'),('unused1',null3)),
                 MelConditions(),
                 ),
             ),
        )
    melSet.loaders = MelQustLoaders(melSet.loaders,*melSet.elements[5:8])
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreRace(MelRecord):
    """Race record.

    This record is complex to read and write. Relatively simple problems are the VNAM
    which can be empty or zeroed depending on relationship between voices and
    the fid for the race.

    The face and body data is much more complicated, with the same subrecord types
    mapping to different attributes depending on preceding flag subrecords (NAM0, NAM1,
    NMAN, FNAM and INDX.) These are handled by using the MelRaceDistributor class
    to dynamically reassign melSet.loaders[type] as the flag records are encountered.

    It's a mess, but this is the shortest, clearest implementation that I could
    think of."""

    classType = 'RACE'
    _flags = Flags(0L,Flags.getNames('playable', None, 'child'))

    class MelRaceVoices(MelStruct):
        """Set voices to zero, if equal race fid. If both are zero, then don't skip dump."""
        def dumpData(self,record,out):
            if record.maleVoice == record.fid: record.maleVoice = 0L
            if record.femaleVoice == record.fid: record.femaleVoice = 0L
            if (record.maleVoice,record.femaleVoice) != (0,0):
                MelStruct.dumpData(self,record,out)

    class MelRaceHeadModel(MelGroup):
        """Most face data, like a MelModel + ICON + MICO. Load is controlled by MelRaceDistributor."""
        def __init__(self,attr,index):
            MelGroup.__init__(self,attr,
                MelString('MODL','modPath'),
                MelBase('MODB','modb_p'),
                MelBase('MODT','modt_p'),
                MelBase('MODS','mods_p'),
                MelOptStruct('MODD','B','modd_p'),
                MelString('ICON','iconPath'),
                MelBase('MICO','mico'))
            self.index = index
        def dumpData(self,record,out):
            out.packSub('INDX','I',self.index)
            MelGroup.dumpData(self,record,out)

    class MelRaceBodyModel(MelGroup):
        """Most body data, like a MelModel - MODB + ICON + MICO. Load is controlled by MelRaceDistributor."""
        def __init__(self,attr,index):
            MelGroup.__init__(self,attr,
                MelString('ICON','iconPath'),
                MelBase('MICO','mico'),
                MelString('MODL','modPath'),
                MelBase('MODT','modt_p'),
                MelBase('MODS','mods_p'),
                MelOptStruct('MODD','B','modd_p'))
            self.index = index
        def dumpData(self,record,out):
            out.packSub('INDX','I',self.index)
            MelGroup.dumpData(self,record,out)

    class MelRaceIcon(MelString):
        """Most body data plus eyes for face. Load is controlled by MelRaceDistributor."""
        def __init__(self,attr,index):
            MelString.__init__(self,'ICON',attr)
            self.index = index
        def dumpData(self,record,out):
            out.packSub('INDX','I',self.index)
            MelString.dumpData(self,record,out)

    class MelRaceFaceGen(MelGroup):
        """Most fecegen data. Load is controlled by MelRaceDistributor."""
        def __init__(self,attr):
            MelGroup.__init__(self,attr,
                MelBase('FGGS','fggs_p'), ####FaceGen Geometry-Symmetric
                MelBase('FGGA','fgga_p'), ####FaceGen Geometry-Asymmetric
                MelBase('FGTS','fgts_p'), ####FaceGen Texture-Symmetric
                MelStruct('SNAM','2s',('snam_p',null2)))

    class MelRaceDistributor(MelNull):
        """Handles NAM0, NAM1, MNAM, FMAN and INDX records. Distributes load
        duties to other elements as needed."""
        def __init__(self):
            headAttrs = ('Head', 'Ears', 'Mouth', 'TeethLower', 'TeethUpper', 'Tongue', 'LeftEye', 'RightEye')
            bodyAttrs = ('UpperBody','LeftHand','RightHand','UpperBodyTexture')
            self.headModelAttrs = {
                'MNAM':tuple('male'+text for text in headAttrs),
                'FNAM':tuple('female'+text for text in headAttrs),
                }
            self.bodyModelAttrs = {
                'MNAM':tuple('male'+text for text in bodyAttrs),
                'FNAM':tuple('female'+text for text in bodyAttrs),
                }
            self.attrs = {
                'NAM0':self.headModelAttrs,
                'NAM1':self.bodyModelAttrs
                }
            self.facegenAttrs = {'MNAM':'maleFaceGen','FNAM':'femaleFaceGen'}
            self._debug = False

        def getSlotsUsed(self):
            return ('_loadAttrs','_modelAttrs')

        def getLoaders(self,loaders):
            """Self as loader for structure types."""
            for type in ('NAM0','NAM1','MNAM','FNAM','INDX'):
                loaders[type] = self

        def setMelSet(self,melSet):
            """Set parent melset. Need this so that can reassign loaders later."""
            self.melSet = melSet
            self.loaders = {}
            for element in melSet.elements:
                attr = element.__dict__.get('attr',None)
                if attr: self.loaders[attr] = element

        def loadData(self,record,ins,type,size,readId):
            if type in ('NAM0','NAM1'):
                record._modelAttrs = self.attrs[type]
                return
            elif type in ('MNAM','FNAM'):
                record._loadAttrs = record._modelAttrs[type]
                attr = self.facegenAttrs.get(type)
                element = self.loaders[attr]
                for type in ('FGGS','FGGA','FGTS','SNAM'):
                    self.melSet.loaders[type] = element
            else: #--INDX
                index, = ins.unpack('I',4,readId)
                attr = record._loadAttrs[index]
                element = self.loaders[attr]
                for type in ('MODL','MODB','MODT','MODS','MODD','ICON','MICO'):
                    self.melSet.loaders[type] = element

    #--Mel Set
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelString('DESC','text'),
        MelStruct('DATA','14b2s4fI','skill1','skill1Boost','skill2','skill2Boost',
                  'skill3','skill3Boost','skill4','skill4Boost','skill5','skill5Boost',
                  'skill6','skill6Boost','skill7','skill7Boost',('unused1',null2),
                  'maleHeight','femaleHeight','maleWeight','femaleWeight',(_flags,'flags',0L)),
        MelFid('ONAM','Older'),
        MelFid('YNAM','Younger'),
        MelBase('NAM2','_nam2',''),
        MelRaceVoices('VTCK','2I',(FID,'maleVoice'),(FID,'femaleVoice')), #--0 same as race fid.
        MelOptStruct('DNAM','2I',(FID,'defaultHairMale',0L),(FID,'defaultHairFemale',0L)), #--0=None
        MelStruct('CNAM','2B','defaultHairColorMale','defaultHairColorFemale'), #--Int corresponding to GMST sHairColorNN
        MelOptStruct('PNAM','f','mainClamp'),
        MelOptStruct('UNAM','f','faceClamp'),
        MelStruct('ATTR','2B','maleBaseAttribute','femaleBaseAttribute'),
        #--Begin Indexed entries
        MelBase('NAM0','_nam0',''), ####Face Data Marker, wbEmpty
        MelBase('MNAM','_mnam',''),
        MelRaceHeadModel('maleHead',0),
        MelRaceIcon('maleEars',1),
        MelRaceHeadModel('maleMouth',2),
        MelRaceHeadModel('maleTeethLower',3),
        MelRaceHeadModel('maleTeethUpper',4),
        MelRaceHeadModel('maleTongue',5),
        MelRaceHeadModel('maleLeftEye',6),
        MelRaceHeadModel('maleRightEye',7),
        MelBase('FNAM','_fnam',''),
        MelRaceHeadModel('femaleHead',0),
        MelRaceIcon('femaleEars',1),
        MelRaceHeadModel('femaleMouth',2),
        MelRaceHeadModel('femaleTeethLower',3),
        MelRaceHeadModel('femaleTeethUpper',4),
        MelRaceHeadModel('femaleTongue',5),
        MelRaceHeadModel('femaleLeftEye',6),
        MelRaceHeadModel('femaleRightEye',7),
        MelBase('NAM1','_nam1',''), ####Body Data Marker, wbEmpty
        MelBase('MNAM','_mnam',''), ####Male Body Data Marker, wbEmpty
        MelRaceBodyModel('maleUpperBody',0),
        MelRaceBodyModel('maleLeftHand',1),
        MelRaceBodyModel('maleRightHand',2),
        MelRaceBodyModel('maleUpperBodyTexture',3),
        MelBase('FNAM','_fnam',''), ####Female Body Data Marker, wbEmpty
        MelRaceBodyModel('femaleUpperBody',0),
        MelRaceBodyModel('femaleLeftHand',1),
        MelRaceBodyModel('femaleRightHand',2),
        MelRaceBodyModel('femaleUpperBodyTexture',3),
        #--Normal Entries
        MelFidList('HNAM','hairs'),
        MelFidList('ENAM','eyes'),
        #--FaceGen Entries
        MelBase('MNAM','_mnam',''),
        MelRaceFaceGen('maleFaceGen'),
        MelBase('FNAM','_fnam',''),
        MelRaceFaceGen('femaleFaceGen'),
        #--Distributor for face and body entries.
        MelRaceDistributor(),
        )
    melSet.elements[-1].setMelSet(melSet)
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreRads(MelRecord):
    """Radiation Stage record."""
    classType = 'RADS'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('DATA','2I','trigerThreshold',(FID,'actorEffect')),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreRcct(MelRecord):
    """Recipe Category."""
    classType = 'RCCT'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelStruct('DATA','=B','flags'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreRcpe(MelRecord):
    """Recipe."""
    classType = 'RCPE'
    class MelRcpeDistributor(MelNull):
        def __init__(self):
            self._debug = False
        def getLoaders(self,loaders):
            """Self as loader for structure types."""
            for type in ('RCQY',):
                loaders[type] = self
        def setMelSet(self,melSet):
            """Set parent melset. Need this so that can reassign loaders later."""
            self.melSet = melSet
            self.loaders = {}
            for element in melSet.elements:
                attr = element.__dict__.get('attr',None)
                if attr: self.loaders[attr] = element
        def loadData(self,record,ins,type,size,readId):
            if type in ('RCQY',):
                outputs = record.__getattribute__('outputs')
                if outputs:
                    element = self.loaders['outputs']
                else:
                    element = self.loaders['ingredients']
            element.loadData(record,ins,type,size,readId)
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelConditions(),
        MelStruct('DATA','4I','skill','level',(FID,'category'),(FID,'subCategory')),
        MelGroups('ingredients',
            MelFid('RCIL','item'),
            MelStruct('RCQY','I','quantity'),
            ),
        MelGroups('outputs',
            MelFid('RCOD','item'),
            MelStruct('RCQY','I','quantity'),
            ),
        MelRcpeDistributor(),
        )
    melSet.elements[-1].setMelSet(melSet)
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreRefr(MelRecord):
    """Placed Object"""
    classType = 'REFR'
    _flags = Flags(0L,Flags.getNames('visible', 'canTravelTo'))
    _parentFlags = Flags(0L,Flags.getNames('oppositeParent'))
    _actFlags = Flags(0L,Flags.getNames('useDefault', 'activate','open','openByDefault'))
    _lockFlags = Flags(0L,Flags.getNames(None, None, 'leveledLock'))
    _destinationFlags = Flags(0L,Flags.getNames('noAlarm'))
    _variableFlags = Flags(0L,Flags.getNames('isLongOrShort'))
    class MelRefrXloc(MelOptStruct):
        """Handle older truncated XLOC for REFR subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 20:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            #elif size == 16:
            #    unpacked = ins.unpack('B3sIB3s',size,readId)
            elif size == 12:
                unpacked = ins.unpack('B3sI4s',size,readId)
            else:
                print ins.unpack(('%dB' % size),size)
                raise ModError(ins.inName,_('Unexpected size encountered for REFR:XLOC subrecord: ')+str(size))
            unpacked = unpacked[:-2] + self.defaults[len(unpacked)-2:-2] + unpacked[-2:]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked

    class MelRefrXmrk(MelStruct):
        """Handler for xmrk record. Conditionally loads next items."""
        def loadData(self,record,ins,type,size,readId):
            """Reads data from ins into record attribute."""
            junk = ins.read(size,readId)
            record.hasXmrk = True
            insTell = ins.tell
            insUnpack = ins.unpack
            pos = insTell()
            (type,size) = insUnpack('4sH',6,readId+'.FULL')
            while type in ['FNAM','FULL','TNAM','WMI1']:
                if type == 'FNAM':
                    value = insUnpack('B',size,readId)
                    record.flags = MreRefr._flags(*value)
                elif type == 'FULL':
                    record.full = ins.readString(size,readId)
                elif type == 'TNAM':
                    record.markerType, record.unused5 = insUnpack('Bs',size,readId)
                elif type == 'WMI1':
                    record.reputation = insUnpack('I',size,readId)
                pos = insTell()
                (type,size) = insUnpack('4sH',6,readId+'.FULL')
            ins.seek(pos)
            if self._debug: print ' ',record.flags,record.full,record.markerType
        def dumpData(self,record,out):
            if (record.flags,record.full,record.markerType,record.unused5,record.reputation) != self.defaults[1:]:
                record.hasXmrk = True
            if record.hasXmrk:
                try:
                    out.write(struct.pack('=4sH','XMRK',0))
                    out.packSub('FNAM','B',record.flags.dump())
                    value = record.full
                    if value != None:
                        out.packSub0('FULL',value)
                    out.packSub('TNAM','Bs',record.markerType, record.unused5)
                    out.packRef('WMI1',record.reputation)
                except struct.error:
                    print self.subType,self.format,record.flags,record.full,record.markerType
                    raise

    melSet = MelSet(
        MelString('EDID','eid'),
        MelOptStruct('RCLR','8B','referenceStartColorRed','referenceStartColorGreen','referenceStartColorBlue',('referenceColorUnused1',null1),
                     'referenceEndColorRed','referenceEndColorGreen','referenceEndColorBlue',('referenceColorUnused2',null1)),
        MelFid('NAME','base'),
        MelFid('XEZN','encounterZone'),
        MelBase('XRGD','ragdollData'),
        MelBase('XRGB','ragdollBipedData'),
        MelOptStruct('XPRM','3f3IfI','primitiveBoundX','primitiveBoundY','primitiveBoundX',
                     'primitiveColorRed','primitiveColorGreen','primitiveColorBlue','primitiveUnknown','primitiveType'),
        MelOptStruct('XTRI','I','collisionLayer'),
        MelBase('XMBP','multiboundPrimitiveMarker'),
        MelOptStruct('XMBO','3f','boundHalfExtentsX','boundHalfExtentsY','boundHalfExtentsZ'),
        MelOptStruct('XTEL','I6fI',(FID,'destinationFid'),'destinationPosX','destinationPosY',
            'destinationPosZ','destinationRotX','destinationRotY','destinationRotZ',(_destinationFlags,'destinationFlags')),
        MelRefrXmrk('XMRK','',('hasXmrk',False),(_flags,'flags',0L),'full','markerType',('unused5',null1),(FID,'reputation')), ####Map Marker Start Marker, wbEmpty
        MelGroup('audioData',
            MelBase('MMRK','audioMarker'),
            MelBase('FULL','full_p'),
            MelFid('CNAM','audioLocation'),
            MelBase('BNAM','bnam_p'),
            MelBase('MNAM','mnam_p'),
            MelBase('NNAM','nnam_p'),
            ),
        MelBase('XSRF','xsrf_p'),
        MelBase('XSRD','xsrd_p'),
        MelFid('XTRG','targetId'),
        MelOptStruct('XLCM','i',('levelMod',None)),
        MelGroup('patrolData',
            MelStruct('XPRD','f','idleTime'),
            MelBase('XPPA','patrolScriptMarker'),
            MelFid('INAM', 'idle'),
            MelStruct('SCHR','4s4I',('unused1',null4),'numRefs','compiledSize','lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_variableFlags,'flags',0L),('unused2',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            MelFid('TNAM','topic'),
            ),
        MelOptStruct('XRDO','fIfI','rangeRadius','broadcastRangeType','staticPercentage',(FID,'positionReference')),
        MelOwnership(),
        MelRefrXloc('XLOC','B3sI4sB3s4s','lockLevel',('unused1',null3),(FID,'lockKey'),('unused2',null4),(_lockFlags,'lockFlags'),('unused3',null3),('unused4',null4)),
        MelOptStruct('XCNT','i','count'),
        MelOptStruct('XRDS','f','radius'),
        MelOptStruct('XHLP','f','health'),
        MelOptStruct('XRAD','f','radiation'),
        MelOptStruct('XCHG','f',('charge',None)),
        MelGroup('ammo',
            MelFid('XAMT','type'),
            MelStruct('XAMC','I','count'),
            ),
        MelStructs('XPWR','II','reflectedByWaters',(FID,'reference'),'type'),
        MelFids('XLTW','litWaters'),
        MelStructs('XDCR','II','linkedDecals',(FID,'reference'),'unknown'), # ??
        MelFid('XLKR','linkedReference'),
        MelOptStruct('XCLP','8B','linkStartColorRed','linkStartColorGreen','linkStartColorBlue',('linkColorUnused1',null1),
                     'linkEndColorRed','linkEndColorGreen','linkEndColorBlue',('linkColorUnused2',null1)),
        MelGroup('activateParents',
            MelStruct('XAPD','B','flags'),
            MelStructs('XAPR','If','activateParentRefs',(FID,'reference'),'delay')
            ),
        MelString('XATO','activationPrompt'),
        MelOptStruct('XESP','IB3s',(FID,'parent'),(_parentFlags,'parentFlags'),('unused6',null3)),
        MelOptStruct('XEMI','I',(FID,'emittance')),
        MelFid('XMBR','multiboundReference'),
        MelOptStruct('XACT','I',(_actFlags,'actFlags',0L)), ####Action Flag
        MelBase('ONAM','onam_p'), ####Open by Default, wbEmpty
        MelBase('XIBS','ignoredBySandbox'),
        MelOptStruct('XNDP','2I',(FID,'navMesh'),'unknown'),
        MelOptStruct('XPOD','II',(FID,'portalDataRoom0'),(FID,'portalDataRoom1')),
        MelOptStruct('XPTL','9f','portalWidth','portalHeight','portalPosX','portalPosY','portalPosZ',
                     'portalRot1','portalRot2','portalRot3','portalRot4'),
        MelBase('XSED','speedTreeSeed'),
        ####SpeedTree Seed, if it's a single byte then it's an offset into the list of seed values in the TREE record
        ####if it's 4 byte it's the seed value directly.
        MelGroup('roomData',
            MelStruct('XRMR','H2s','linkedRoomsCount','unknown'),
            MelFids('XLRM','linkedRoom'),
            ),
        MelOptStruct('XOCP','9f','occlusionPlaneWidth','occlusionPlaneHeight','occlusionPlanePosX','occlusionPlanePosY','occlusionPlanePosZ',
                     'occlusionPlaneRot1','occlusionPlaneRot2','occlusionPlaneRot3','occlusionPlaneRot4'),
        MelOptStruct('XORD','4I',(FID,'linkedOcclusionPlane0'),(FID,'linkedOcclusionPlane1'),(FID,'linkedOcclusionPlane2'),(FID,'linkedOcclusionPlane3')),
        MelOptStruct('XLOD','3f',('lod1',None),('lod2',None),('lod3',None)), ####Distant LOD Data, unknown
        MelOptStruct('XSCL','f',('scale',1.0)),
        MelOptStruct('DATA','=6f',('posX',None),('posY',None),('posZ',None),('rotX',None),('rotY',None),('rotZ',None)),

        ##Oblivion subrecords
        #MelOptStruct('XHLT','i',('health',None)),
        #MelXpci('XPCI'), ####fid, unknown
        #MelFid('XRTM','xrtm'), ####unknown
        #MelOptStruct('XSOL','B',('soul',None)), ####Was entirely missing. Confirmed by creating a test mod...it isn't present in any of the official esps
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreRegn(MelRecord):
    """Region record."""
    classType = 'REGN'
    obflags = Flags(0L,Flags.getNames(
        ( 0,'conform'),
        ( 1,'paintVertices'),
        ( 2,'sizeVariance'),
        ( 3,'deltaX'),
        ( 4,'deltaY'),
        ( 5,'deltaZ'),
        ( 6,'Tree'),
        ( 7,'hugeRock'),))
    sdflags = Flags(0L,Flags.getNames(
        ( 0,'pleasant'),
        ( 1,'cloudy'),
        ( 2,'rainy'),
        ( 3,'snowy'),))
    rdatFlags = Flags(0L,Flags.getNames(
        ( 0,'Override'),))

    ####Lazy hacks to correctly read/write regn data
    class MelRegnStructA(MelStructA):
        """Handler for regn record. Conditionally dumps next items."""
        def loadData(self,record,ins,type,size,readId):
            if record.entryType == 2 and self.subType == 'RDOT':
                MelStructA.loadData(self,record,ins,type,size,readId)
            elif record.entryType == 3 and self.subType == 'RDWT':
                MelStructA.loadData(self,record,ins,type,size,readId)
            elif record.entryType == 6 and self.subType == 'RDGS':
                MelStructA.loadData(self,record,ins,type,size,readId)
            elif record.entryType == 7 and self.subType == 'RDSD':
                MelStructA.loadData(self,record,ins,type,size,readId)

        def dumpData(self,record,out):
            """Conditionally dumps data."""
            if record.entryType == 2 and self.subType == 'RDOT':
                MelStructA.dumpData(self,record,out)
            elif record.entryType == 3 and self.subType == 'RDWT':
                MelStructA.dumpData(self,record,out)
            elif record.entryType == 6 and self.subType == 'RDGS':
                MelStructA.dumpData(self,record,out)
            elif record.entryType == 7 and self.subType == 'RDSD':
                MelStructA.dumpData(self,record,out)

    class MelRegnString(MelString):
        """Handler for regn record. Conditionally dumps next items."""
        def loadData(self,record,ins,type,size,readId):
            if record.entryType == 4 and self.subType == 'RDMP':
                MelString.loadData(self,record,ins,type,size,readId)
            elif record.entryType == 5 and self.subType == 'ICON':
                MelString.loadData(self,record,ins,type,size,readId)

        def dumpData(self,record,out):
            """Conditionally dumps data."""
            if record.entryType == 4 and self.subType == 'RDMP':
                MelString.dumpData(self,record,out)
            elif record.entryType == 5 and self.subType == 'ICON':
                MelString.dumpData(self,record,out)

    class MelRegnOptStruct(MelOptStruct):
        """Handler for regn record. Conditionally dumps next items."""
        def loadData(self,record,ins,type,size,readId):
            if record.entryType == 7 and self.subType == 'RDMD':
                MelOptStruct.loadData(self,record,ins,type,size,readId)

        def dumpData(self,record,out):
            """Conditionally dumps data."""
            if record.entryType == 7 and self.subType == 'RDMD':
                MelOptStruct.dumpData(self,record,out)

    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelStruct('RCLR','3Bs','mapRed','mapBlue','mapGreen',('unused1',null1)),
        MelFid('WNAM','worldspace'),
        MelGroups('areas',
            MelStruct('RPLI','I','edgeFalloff'),
            MelStructA('RPLD','2f','points','posX','posY')),
        MelGroups('entries',
            #2:Objects,3:Weather,4:Map,5:Land,6:Grass,7:Sound
            MelStruct('RDAT', 'I2B2s','entryType', (rdatFlags,'flags'), 'priority',
                     ('unused1',null2)),
            MelRegnStructA('RDOT', 'IH2sf4B2H4s4f3H2s4s', 'objects', (FID,'objectId'),
                           'parentIndex',('unused1',null2), 'density', 'clustering',
                           'minSlope', 'maxSlope',(obflags, 'flags'), 'radiusWRTParent',
                           'radius', ('unk1',null4),'maxHeight', 'sink', 'sinkVar',
                           'sizeVar', 'angleVarX','angleVarY',  'angleVarZ',
                           ('unused2',null2), ('unk2',null4)),
            MelRegnString('RDMP', 'mapName'),
            MelRegnStructA('RDGS', 'I4s', 'grass', ('unknown',null4)),
            MelRegnOptStruct('RDMD', 'I', 'musicType'),
            MelFid('RDMO','music'),
            MelFid('RDSI','incidentalMediaSet'),
            MelFids('RDSB','battleMediaSets'),
            MelRegnStructA('RDSD', '3I', 'sounds', (FID, 'sound'), (sdflags, 'flags'), 'chance'),
            MelRegnStructA('RDWT', '3I', 'weather', (FID, 'weather', None), 'chance', (FID, 'global', None)),
            MelFidList('RDID','imposters')),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreRepu(MelRecord):
    """Reputation."""
    classType = 'REPU'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelStruct('DATA','f','value'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreRgdl(MelRecord):
    """Ragdoll"""
    classType = 'RGDL'
    _flags = Flags(0L,Flags.getNames('disableOnMove'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('NVER','I','version'),
        MelStruct('DATA','I4s5Bs','boneCount','unused1','feedback',
            'footIK','lookIK','grabIK','poseMatching','unused2'),
        MelFid('XNAM','actorBase'),
        MelFid('TNAM','bodyPartData'),
        MelStruct('RAFD','13f2i','keyBlendAmount','hierarchyGain','positionGain',
            'velocityGain','accelerationGain','snapGain','velocityDamping',
            'snapMaxLinearVelocity','snapMaxAngularVelocity','snapMaxLinearDistance',
            'snapMaxAngularDistance','posMaxVelLinear',
            'posMaxVelAngular','posMaxVelProjectile','posMaxVelMelee'),
        MelStructA('RAFB','H','feedbackDynamicBones','bone'),
        MelStruct('RAPS','3HBs4f','matchBones1','matchBones2','matchBones3',
            (_flags,'flags'),'unused3','motorsStrength',
            'poseActivationDelayTime','matchErrorAllowance',
            'displacementToDisable',),
        MelString('ANAM','deathPose'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreScpt(MelRecord):
    """Script record."""
    classType = 'SCPT'
    _flags = Flags(0L,Flags.getNames('isLongOrShort'))
    schrFlags = Flags(0L,Flags.getNames('enabled'))
    melSet = MelSet(
        MelString('EDID','eid'),
        #scriptType:0:Object,1:Quest,0x100:Magic Effect
        MelStruct('SCHR','4s3I2H',('unused1',null4),'numRefs','compiledSize',
                  'lastIndex','scriptType',(schrFlags,'enableflag',0L),),
        MelBase('SCDA','compiled_p'),
        MelString('SCTX','scriptText'),
        MelGroups('vars',
            MelStruct('SLSD','I12sB7s','index',('unused1',null4+null4+null4),(_flags,'flags',0L),('unused2',null4+null3)),
            MelString('SCVR','name')),
        MelScrxen('SCRV/SCRO','references'),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreScol(MelRecord):
    """Static Collection"""
    classType = 'SCOL'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelModel(),
        MelGroups('parts',
            MelFid('ONAM','static'),
            MelStructA('DATA','=7f','placement',('posX',None),('posY',None),('posZ',None),('rotX',None),('rotY',None),('rotZ',None),('scale',None),),
        ),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreSlpd(MelRecord):
    """Sleep deprivation stage record."""
    classType = 'SLPD'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('DATA','2I','trigerThreshold',(FID,'actorEffect')),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreSoun(MelRecord):
    """Sound record."""
    classType = 'SOUN'

    # {0x0001} 'Random Frequency Shift',
    # {0x0002} 'Play At Random',
    # {0x0004} 'Environment Ignored',
    # {0x0008} 'Random Location',
    # {0x0010} 'Loop',
    # {0x0020} 'Menu Sound',
    # {0x0040} '2D',
    # {0x0080} '360 LFE',
    # {0x0100} 'Dialogue Sound',
    # {0x0200} 'Envelope Fast',
    # {0x0400} 'Envelope Slow',
    # {0x0800} '2D Radius',
    # {0x1000} 'Mute When Submerged',
    # {0x2000} 'Start at Random Position'
    _flags = Flags(0L,Flags.getNames(
            'randomFrequencyShift',
            'playAtRandom',
            'environmentIgnored',
            'randomLocation',
            'loop',
            'menuSound',
            'twoD',
            'three60LFE',
            'dialogueSound',
            'envelopeFast',
            'envelopeSlow',
            'twoDRadius',
            'muteWhenSubmerged',
            'startatRandomPosition',
        ))

    class MelSounSndx(MelStruct):
        """SNDX is a reduced version of SNDD. Allow it to read in, but not set defaults or write."""
        def loadData(self,record,ins,type,size,readId):
            MelStruct.loadData(self,record,ins,type,size,readId)
            record.point0 = 0
            record.point1 = 0
            record.point2 = 0
            record.point3 = 0
            record.point4 = 0
            record.reverb = 0
            record.priority = 0
            record.xLoc = 0
            record.yLoc = 0
        def getSlotsUsed(self):
            return ()
        def setDefault(self,record): return
        def dumpData(self,record,out): return

    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FNAM','soundFile'),
        MelStruct('RNAM','B','_rnam'),
        MelOptStruct('SNDD','=2BbsIh2B6h3i',('minDist',0), ('maxDist',0),
                    ('freqAdj',0), ('unusedSndd',null1),(_flags,'flags',0L),
                    ('staticAtten',0),('stopTime',0),('startTime',0),
                    ('point0',0),('point1',0),('point2',0),('point3',0),('point4',0),
                    ('reverb',0),('priority',0), ('xLoc',0), ('yLoc',0),),
        MelSounSndx('SNDX','=2BbsIh2B',('minDist',0), ('maxDist',0),
                   ('freqAdj',0), ('unusedSndd',null1),(_flags,'flags',0L),
                   ('staticAtten',0),('stopTime',0),('startTime',0),),
        MelBase('ANAM','_anam'), #--Should be a struct. Maybe later.
        MelBase('GNAM','_gnam'), #--Should be a struct. Maybe later.
        MelBase('HNAM','_hnam'), #--Should be a struct. Maybe later.
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreSpel(MelRecord,MreHasEffects):
    """Actor Effect"""
    classType = 'SPEL'
    class SpellFlags(Flags):
        """For SpellFlags, immuneSilence activates bits 1 AND 3."""
        def __setitem__(self,index,value):
            setter = Flags.__setitem__
            setter(self,index,value)
            if index == 1:
                setter(self,3,value)
    flags = SpellFlags(0L,Flags.getNames('noAutoCalc', 'immuneToSilence',
        'startSpell',None,'ignoreLOS','scriptEffectAlwaysApplies',
        'disallowAbsorbReflect','touchExplodesWOTarget'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelFull0(),
        MelStruct('SPIT','3IB3s','spellType','cost','level',(flags,'flags',0L),('unused1',null3)),
        # spellType = 0: Spell, 1: Disease, 3: Lesser Power, 4: Ability, 5: Poison
        MelEffects(),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreStat(MelRecord):
    """Static model record."""
    classType = 'STAT'

    # passthroughSound
    # -1, 'NONE'
    #  0, 'BushA',
    #  1, 'BushB',
    #  2, 'BushC',
    #  3, 'BushD',
    #  4, 'BushE',
    #  5, 'BushF',
    #  6, 'BushG',
    #  7, 'BushH',
    #  8, 'BushI',
    #  9, 'BushJ'

    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelModel(),
        MelStruct('BRUS','=b',('passthroughSound',-1)),
        MelFid('RNAM','soundRandomLooping'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreTact(MelRecord):
    """Talking activator record."""
    classType = 'TACT'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel('model'),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelFid('SNAM','sound'),
        MelFid('VNAM','voiceType'),
        MelFid('INAM','radioTemplate'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreTerm(MelRecord):
    """Terminal record."""
    classType = 'TERM'
    _flags = Flags(0L,Flags.getNames('leveled','unlocked','alternateColors','hideWellcomeTextWhenDisplayingImage'))
    _menuFlags = Flags(0L,Flags.getNames('addNote','forceRedraw'))
    _variableFlags = Flags(0L,Flags.getNames('isLongOrShort'))
    class MelTermDnam(MelStruct):
        """Handle older truncated DNAM for TERM subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 4:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 3:
                unpacked = ins.unpack('BBB',size,readId)
            else:
                raise "Unexpected size encountered for TERM:DNAM subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel(),
        MelFid('SCRI','script'),
        MelDestructible(),
        MelString('DESC','description'),
        MelFid('SNAM','soundLooping'),
        MelFid('PNAM','passwordNote'),
        MelTermDnam('DNAM','BBBs','baseHackingDifficulty',(_flags,'flags'),
                    'serverType','unused1',),
        MelGroups('menuItems',
            MelString('ITXT','itemText'),
            MelString('RNAM','resultText'),
            MelStruct('ANAM','B',(_menuFlags,'menuFlags')),
            MelFid('INAM','displayNote'),
            MelFid('TNAM','subMenu'),
            MelStruct('SCHR','4s4I',('unused2',null4),'numRefs','compiledSize',
                      'lastIndex','scriptType'),
            MelBase('SCDA','compiled_p'),
            MelString('SCTX','scriptText'),
            MelGroups('vars',
                MelStruct('SLSD','I12sB7s','index',('unused3',null4+null4+null4),
                         (_variableFlags,'flags',0L),('unused4',null4+null3)),
                MelString('SCVR','name')),
            MelScrxen('SCRV/SCRO','references'),
            MelConditions(),
        ),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreTes4(MelRecord):
    """TES4 Record. File header."""
    classType = 'TES4' #--Used by LoadFactory
    #--Masters array element
    class MelTes4Name(MelBase):
        def setDefault(self,record):
            record.masters = []
        def loadData(self,record,ins,type,size,readId):
            name = GPath(ins.readString(size,readId))
            record.masters.append(name)
        def dumpData(self,record,out):
            pack1 = out.packSub0
            pack2 = out.packSub
            for name in record.masters:
                pack1('MAST',name.s)
                pack2('DATA','Q',0)
    #--Data elements
    melSet = MelSet(
        MelStruct('HEDR','f2I',('version',0.8),'numRecords',('nextObject',0xCE6)),
        MelBase('OFST','ofst_p',), #--Obsolete?
        MelBase('DELE','dele_p'), #--Obsolete?
        MelString('CNAM','author','',512),
        MelString('SNAM','description','',512),
        MelTes4Name('MAST','masters'),
        MelBase('ONAM','onam'),
        MelNull('DATA'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

    def getNextObject(self):
        """Gets next object index and increments it for next time."""
        self.changed = True
        self.nextObject += 1
        return (self.nextObject -1)

#------------------------------------------------------------------------------
class MreTree(MelRecord):
    """Tree record."""
    classType = 'TREE'
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelModel(),
        MelString('ICON','iconPath'),
        MelStructA('SNAM','I','speedTree','seed'),
        MelStruct('CNAM','5fi2f', 'curvature','minAngle','maxAngle',
                  'branchDim','leafDim','shadowRadius','rockSpeed',
                  'rustleSpeed'),
        MelStruct('BNAM','2f','widthBill','heightBill'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreTxst(MelRecord):
    """Texture set record."""
    classType = 'TXST'
    TxstTypeFlags = Flags(0L,Flags.getNames(
        (0, 'noSpecularMap'),
    ))

    DecalDataFlags = Flags(0L,Flags.getNames(
            (0, 'parallax'),
            (0, 'alphaBlending'),
            (0, 'alphaTesting'),
            (0, 'noSubtextures'),
        ))

    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('TX00','baseImage'),
        MelString('TX01','normalMap'),
        MelString('TX02','environmentMapMask'),
        MelString('TX03','growMap'),
        MelString('TX04','parallaxMap'),
        MelString('TX05','environmentMap'),
        MelOptStruct('DODT','7fBB2s3Bs','minWidth','maxWidth','minHeight',
                     'maxHeight','depth','shininess','parallaxScale',
                     'parallaxPasses',(DecalDataFlags,'flags',0L),
                     ('unused1',null2),'red','green','blue',('unused2',null1)),
        MelStruct('DNAM','H',(TxstTypeFlags,'flags',0L),),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreVtyp(MelRecord):
    """Voice type record."""
    classType = 'VTYP'
    _flags = Flags(0L,Flags.getNames('allowDefaultDialog','female'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('DNAM','B',(_flags,'flags')),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreWatr(MelRecord):
    """Water record."""
    classType = 'WATR'
    _flags = Flags(0L,Flags.getNames('causesDmg','reflective'))
    class MelWatrData(MelStruct):
        """Handle older truncated DATA for WATR subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 186:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 2:
                (record.damage,) = ins.unpack('H',size,readId)
                return
            else:
                raise "Unexpected size encountered for WATR subrecord: %s" % size
        def dumpData(self,record,out):
            out.packSub(self.subType,'H',record.damage)

    class MelWatrDnam(MelStruct):
        """Handle older truncated DNAM for WATR subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 196:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 184:
                unpacked = ins.unpack('10f3Bs3Bs3BsI32f',size,readId)
            else:
                raise ModError(ins.inName,_('Unexpected size encountered for WATR subrecord: ')+str(size))
            unpacked = unpacked[:-1]
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked

    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelString('NNAM','texture'),
        MelStruct('ANAM','B','opacity'),
        MelStruct('FNAM','B',(_flags,'flags',0)),
        MelString('MNAM','material'),
        MelFid('SNAM','sound',),
        MelFid('XNAM','effect'),
        MelWatrData('DATA','10f3Bs3Bs3BsI32fH',('windVelocity',0.100),('windDirection',90.0),
            ('waveAmp',0.5),('waveFreq',1.0),('sunPower',50.0),('reflectAmt',0.5),
            ('fresnelAmt',0.0250),('unknown1',0.0),('fogNear',27852.8),('fogFar',163840.0),
            ('shallowRed',0),('shallowGreen',128),('shallowBlue',128),('unused1',null1),
            ('deepRed',0),('deepGreen',0),('deepBlue',25),('unused2',null1),
            ('reflRed',255),('reflGreen',255),('reflBlue',255),('unused3',null1),
            ('unknown2',0),
            ('rainForce',0.1000),('rainVelocity',0.6000),('rainFalloff',0.9850),('rainDampner',2.0000),('rainSize',0.0100),
            ('dispForce',0.4000),('dispVelocity', 0.6000),('dispFalloff',0.9850),('dispDampner',10.0000),('dispSize',0.0500),
            ('noiseNormalsScale',1.8000),('noiseLayer1WindDirection',0.0000),('noiseLayer2WindDirection',-431602080.0500),
            ('noiseLayer3WindDirection',-431602080.0500),('noiseLayer1WindVelocity',0.0000),
            ('noiseLayer2WindVelocity',-431602080.0500),('noiseLayer3WindVelocity',-431602080.0500),
            ('noiseNormalsDepthFalloffStart',0.00000),('noiseNormalsDepthFalloffEnd',0.10000),
            ('fogAboveWaterAmount',1.00000),('noiseNormalsUvScale',500.00000),
            ('fogUnderWaterAmount',1.00000),('fogUnderWaterNear',0.00000),('fogUnderWaterFar',1000.00000),
            ('distortionAmount',250.00000),('shininess',100.00000),('reflectHdrMult',1.00000),
            ('lightRadius',10000.00000),('lightBrightness',1.00000),
            ('noiseLayer1UvScale',100.00000),('noiseLayer2UvScale',100.00000),('noiseLayer3UvScale',100.00000),
            ('damage',0)),
        MelWatrDnam('DNAM','10f3Bs3Bs3BsI35f',('windVelocity',0.100),('windDirection',90.0),
            ('waveAmp',0.5),('waveFreq',1.0),('sunPower',50.0),('reflectAmt',0.5),
            ('fresnelAmt',0.0250),('unknown1',0.0),('fogNear',27852.8),('fogFar',163840.0),
            ('shallowRed',0),('shallowGreen',128),('shallowBlue',128),('unused1',null1),
            ('deepRed',0),('deepGreen',0),('deepBlue',25),('unused2',null1),
            ('reflRed',255),('reflGreen',255),('reflBlue',255),('unused3',null1),
            ('unknown2',0),
            ('rainForce',0.1000),('rainVelocity',0.6000),('rainFalloff',0.9850),('rainDampner',2.0000),('rainSize',0.0100),
            ('dispForce',0.4000),('dispVelocity', 0.6000),('dispFalloff',0.9850),('dispDampner',10.0000),('dispSize',0.0500),
            ('noiseNormalsScale',1.8000),('noiseLayer1WindDirection',0.0000),('noiseLayer2WindDirection',-431602080.0500),
            ('noiseLayer3WindDirection',-431602080.0500),('noiseLayer1WindVelocity',0.0000),
            ('noiseLayer2WindVelocity',-431602080.0500),('noiseLayer3WindVelocity',-431602080.0500),
            ('noiseNormalsDepthFalloffStart',0.00000),('noiseNormalsDepthFalloffEnd',0.10000),
            ('fogAboveWaterAmount',1.00000),('noiseNormalsUvScale',500.00000),
            ('fogUnderWaterAmount',1.00000),('fogUnderWaterNear',0.00000),('fogUnderWaterFar',1000.00000),
            ('distortionAmount',250.00000),('shininess',100.00000),('reflectHdrMult',1.00000),
            ('lightRadius',10000.00000),('lightBrightness',1.00000),
            ('noiseLayer1UvScale',100.00000),('noiseLayer2UvScale',100.00000),('noiseLayer3UvScale',100.00000),
            ('noiseLayer1Amp',0.00000),('noiseLayer2Amp',0.00000),('noiseLayer3Amp',0.00000),
            ),
        MelFidList('GNAM','relatedWaters'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreWeap(MelRecord):
    """Weapon record."""
    classType = 'WEAP'
    _flags = Flags(0L,Flags.getNames('notNormalWeapon'))
    _dflags1 = Flags(0L,Flags.getNames(
            'ignoresNormalWeaponResistance',
            'isAutomatic',
            'hasScope',
            'cantDrop',
            'hideBackpack',
            'embeddedWeapon',
            'dontUse1stPersonISAnimations',
            'nonPlayable',
        ))
    _dflags2 = Flags(0L,Flags.getNames(
            'playerOnly',
            'npcsUseAmmo',
            'noJamAfterReload',
            'overrideActionPoint',
            'minorCrime',
            'rangeFixed',
            'notUseInNormalCombat',
            'overrideDamageToWeaponMult',
            'dontUse3rdPersonISAnimations',
            'shortBurst',
            'RumbleAlternate',
            'longBurst',
            'scopeHasNightVision',
            'scopeFromMod',
        ))
    _cflags = Flags(0L,Flags.getNames(
            'onDeath',
            'unknown1','unknown2','unknown3','unknown4',
            'unknown5','unknown6','unknown7',
        ))

    class MelWeapDnam(MelStruct):
        """Handle older truncated DNAM for WEAP subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 204:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 200:
                unpacked = ins.unpack('I2f4B5fI4B2f2I11fiI2fi4f3I3f2IsB2s6f',size,readId)
            elif size == 196:
                unpacked = ins.unpack('I2f4B5fI4B2f2I11fiI2fi4f3I3f2IsB2s5f',size,readId)
            elif size == 180:
                unpacked = ins.unpack('I2f4B5fI4B2f2I11fiI2fi4f3I3f2IsB2sf',size,readId)
            elif size == 172:
                unpacked = ins.unpack('I2f4B5fI4B2f2I11fiI2fi4f3I3f2I',size,readId)
            elif size == 164:
                unpacked = ins.unpack('I2f4B5fI4B2f2I11fiI2fi4f3I3f',size,readId)
            elif size == 136:
                unpacked = ins.unpack('I2f4B5fI4B2f2I11fiI2fi3f',size,readId)
            elif size == 124:
                #--Else 124 byte record (skips sightUsage, semiAutomaticFireDelayMin and semiAutomaticFireDelayMax...
                unpacked = ins.unpack('I2f4B5fI4B2f2I11fiI2fi',size,readId)
            elif size == 120:
                #--Else 120 byte record (skips resistType, sightUsage, semiAutomaticFireDelayMin and semiAutomaticFireDelayMax...
                unpacked = ins.unpack('I2f4B5fI4B2f2I11fiI2f',size,readId)
            else:
                raise "Unexpected size encountered for WEAP:DNAM subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked

    class MelWeapVats(MelStruct):
        """Handle older truncated VATS for WEAP subrecord."""
        def loadData(self,record,ins,type,size,readId):
            if size == 20:
                MelStruct.loadData(self,record,ins,type,size,readId)
                return
            elif size == 16:
                unpacked = ins.unpack('Ifff',size,readId)
            else:
                raise "Unexpected size encountered for WEAP:VATS subrecord: %s" % size
            unpacked += self.defaults[len(unpacked):]
            setter = record.__setattr__
            for attr,value,action in zip(self.attrs,unpacked,self.actions):
                if callable(action): value = action(value)
                setter(attr,value)
            if self._debug: print unpacked

    melSet = MelSet(
        MelString('EDID','eid'),
        MelStruct('OBND','=6h',
                  'boundX1','boundY1','boundZ1',
                  'boundX2','boundY2','boundZ2'),
        MelString('FULL','full'),
        MelModel('model'),
        MelString('ICON','iconPath'),
        MelString('MICO','smallIconPath'),
        MelFid('SCRI','script'),
        MelFid('EITM','enchantment'),
        MelOptStruct('EAMT','H', 'enchantPoints'),
        MelFid('NAM0','ammo'),
        MelDestructible(),
        MelFid('REPL','repairList'),
        #-1:None,0:Big Guns,1:Energy Weapons,2:Small Guns,3:Melee Weapons,
        #4:Unarmed Weapon,5:Thrown Weapons,6:Mine,7:Body Wear,8:Head Wear,
        #9:Hand Wear,10:Chems,11:Stimpack,12:Food,13:Alcohol
        MelStruct('ETYP','i',('etype',-1)),
        MelFid('BIPL','bipedModelList'),
        MelFid('YNAM','pickupSound'),
        MelFid('ZNAM','dropSound'),
        MelModel('shellCasingModel',2),
        MelModel('scopeModel',3),
        MelFid('EFSD','scopeEffect'),
        MelModel('worldModel',4),
        MelGroup('modelWithMods',
                 MelString('MWD1','mod1Path'),
                 MelString('MWD2','mod2Path'),
                 MelString('MWD3','mod1and2Path'),
                 MelString('MWD4','mod3Path'),
                 MelString('MWD5','mod1and3Path'),
                 MelString('MWD6','mod2and3Path'),
                 MelString('MWD7','mod1and2and3Path'),
                 ),
        MelString('VANM','vatsAttackName'),
        MelString('NNAM','embeddedWeaponNode'),
        MelFid('INAM','impactDataset'),
        MelFid('WNAM','firstPersonModel'),
        MelGroup('firstPersonModelWithMods',
                 MelFid('WNM1','mod1Path'),
                 MelFid('WNM2','mod2Path'),
                 MelFid('WNM3','mod1and2Path'),
                 MelFid('WNM4','mod3Path'),
                 MelFid('WNM5','mod1and3Path'),
                 MelFid('WNM6','mod2and3Path'),
                 MelFid('WNM7','mod1and2and3Path'),
                 ),
        MelGroup('weaponMods',
                 MelFid('WMI1','mod1'),
                 MelFid('WMI2','mod2'),
                 MelFid('WMI3','mod3'),
                 ),
        MelFids('SNAM','soundGunShot3D'),
        MelFid('XNAM','soundGunShot2D'),
        MelFid('NAM7','soundGunShot3DLooping'),
        MelFid('TNAM','soundMeleeSwingGunNoAmmo'),
        MelFid('NAM6','soundBlock'),
        MelFid('UNAM','idleSound',),
        MelFid('NAM9','equipSound',),
        MelFid('NAM8','unequipSound',),
        MelFids('WMS1','soundMod1Shoot3Ds'),
        MelFid('WMS2','soundMod1Shoot2D'),
        MelStruct('DATA','2IfHB','value','health','weight','damage','clipsize'),
        MelWeapDnam('DNAM','I2f4B4f4sI4B2f2I11fiI2fi3f4s3I3f2IsB2s6fI',
                    'animationType','animationMultiplier','reach',
                    (_dflags1,'dnamFlags1',0L),'gripAnimation','ammoUse',
                    'reloadAnimation','minSpread','spread','unknown','sightFov',
                    'unknown2',(FID,'projectile',0L),'baseVatsToHitChance',
                    'attackAnimation','projectileCount','embeddedWeaponActorValue',
                    'minRange','maxRange','onHit',(_dflags2,'dnamFlags2',0L),
                    'animationAttackMultiplier','fireRate','overrideActionPoint',
                    'rumbleLeftMotorStrength','rumbleRightMotorStrength',
                    'rumbleDuration','overrideDamageToWeaponMult','attackShotsPerSec',
                    'reloadTime','jamTime','aimArc','skill','rumblePattern',
                    'rambleWavelangth','limbDmgMult',('resistType',0xFFFFFFFF),
                    'sightUsage','semiAutomaticFireDelayMin',
                    'semiAutomaticFireDelayMax',
                    # NV additions
                    'unknown3','effectMod1','effectMod2','effectMod3','valueAMod1',
                    'valueAMod2','valueAMod3','powerAttackAnimation','strengthReq',
                    ('unknown4',null1),'reloadAnimationMod',('unknown5',null2),
                    'regenRate','killImpulse','valueBMod1','valueBMod2','valueBMod3',
                    'impulseDist','skillReq'),
        MelStruct('CRDT','H2sfB3sI','criticalDamage','unknown3','criticalMultiplier',
                 (_cflags,'criticalFlags',0L),'unknown4',(FID,'criticalEffect',0L)),
        MelWeapVats('VATS','I3f2B2s','vatsEffect','vatsSkill','vatsDamMult',
                    'vatsAp','vatsSilent','vatsModReqiured',('unused1',null2)),
        MelBase('VNAM','soundLevel'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MreWrld(MelRecord):
    """Worldspace record."""
    classType = 'WRLD'
    _flags = Flags(0L,Flags.getNames('smallWorld','noFastTravel','oblivionWorldspace',None,
        'noLODWater','noLODNoise','noAllowNPCFallDamage'))
    pnamFlags = Flags(0L,Flags.getNames(
        'useLandData','useLODData','useMapData','useWaterData','useClimateData',
        'useImageSpaceData',None,'needsWaterAdjustment'))
    melSet = MelSet(
        MelString('EDID','eid'),
        MelString('FULL','full'),
        MelFid('XEZN','encounterZone'),
        MelFid('WNAM','parent'),
        MelOptStruct('PNAM','BB',(pnamFlags,'parentFlags',0L),('unknownff',0xff)),
        MelFid('CNAM','climate'),
        MelFid('NAM2','water'),
        MelFid('NAM3','waterType'),
        MelStruct('NAM4','f','waterHeight'),
        MelStruct('DNAM','ff','defaultLandHeight','defaultWaterHeight'),
        MelString('ICON','mapPath'),
        MelOptStruct('MNAM','2i4h',('dimX',None),('dimY',None),('NWCellX',None),('NWCellY',None),('SECellX',None),('SECellY',None)),
        MelStruct('ONAM','fff','worldMapScale','cellXOffset','cellYOffset'),
        MelFid('INAM','imageSpace'),
        MelStruct('DATA','B',(_flags,'flags',0L)),
        MelTuple('NAM0','ff','unknown0',(None,None)),
        MelTuple('NAM9','ff','unknown9',(None,None)),
        MelFid('ZNAM','music'),
        MelString('NNAM','canopyShadow'),
        MelString('XNAM','waterNoiseTexture'),
        MelStructs('IMPS','III','swappedImpacts', 'materialType',(FID,'old'),(FID,'new')),
        MelBase('IMPF','footstepMaterials'), #--todo rewrite specific class.
        MelBase('OFST','ofst_p'),
    )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
class MelPnamNam0Handler(MelStructA):
    """Handle older truncated PNAM for WTHR subrecord."""
    def __init__(self,type,attr):
        MelStructA.__init__(self,type,'3Bs3Bs3Bs3Bs3Bs3Bs',attr,
            'riseRed','riseGreen','riseBlue',('unused1',null1),
            'dayRed','dayGreen','dayBlue',('unused2',null1),
            'setRed','setGreen','setBlue',('unused3',null1),
            'nightRed','nightGreen','nightBlue',('unused4',null1),
            'noonRed','noonGreen','noonBlue',('unused5',null1),
            'midnightRed','midnightGreen','midnightBlue',('unused6',null1),
            )

    def loadData(self,record,ins,type,size,readId):
        """Handle older truncated PNAM for WTHR subrecord."""
        if (type == 'PNAM' and size == 96) or (type == 'NAM0' and size == 240):
            MelStructA.loadData(self,record,ins,type,size,readId)
            return
        elif (type == 'PNAM' and size == 64) or (type == 'NAM0' and size == 160):
            oldFormat = '3Bs3Bs3Bs3Bs'
            ## Following code works completely, but it's depend on the implementation of MelStructA.loadData and MelStruct.loadData.
            # newFormat = self.format
            # self.format = oldFormat # temporarily set to older format
            # MelStructA.loadData(self,record,ins,type,size,readId)
            # self.format = newFormat
            ## Following code is redundant but independent and robust.
            selfDefault = self.getDefault
            recordAppend = record.__getattribute__(self.attr).append
            selfAttrs = self.attrs
            itemSize = struct.calcsize(oldFormat)
            for x in xrange(size/itemSize):
                target = selfDefault()
                recordAppend(target)
                target.__slots__ = selfAttrs
                unpacked = ins.unpack(oldFormat,itemSize,readId)
                setter = target.__setattr__
                for attr,value,action in zip(selfAttrs,unpacked,self.actions):
                    if action: value = action(value)
                    setter(attr,value)
        else:
            raise ModSizeError(record.inName,record.recType+'.'+type,(96 if type == 'PNAM' else 240),size,True)

class MreWthr(MelRecord):
    """Weather record."""
    classType = 'WTHR'

    melSet = MelSet(
        MelString('EDID','eid'),
        MelFid("\x00IAD", 'sunriseImageSpaceModifier'),
        MelFid("\x01IAD", 'dayImageSpaceModifier'),
        MelFid("\x02IAD", 'sunsetImageSpaceModifier'),
        MelFid("\x03IAD", 'nightImageSpaceModifier'),
        MelFid("\x04IAD", 'unknown1ImageSpaceModifier'),
        MelFid("\x05IAD", 'unknown2ImageSpaceModifier'),
        MelString('DNAM','upperLayer'),
        MelString('CNAM','lowerLayer'),
        MelString('ANAM','layer2'),
        MelString('BNAM','layer3'),
        MelModel(),
        MelBase('LNAM','unknown1'),
        MelStruct('ONAM','4B','cloudSpeed0','cloudSpeed1','cloudSpeed3','cloudSpeed4'),
        MelPnamNam0Handler('PNAM','cloudColors'),
        MelPnamNam0Handler('NAM0','daytimeColors'),
        MelStruct('FNAM','6f','fogDayNear','fogDayFar','fogNightNear','fogNightFar','fogDayPower','fogNightPower'),
        MelBase('INAM','_inam'), #--Should be a struct. Maybe later.
        MelStruct('DATA','15B',
            'windSpeed','lowerCloudSpeed','upperCloudSpeed','transDelta',
            'sunGlare','sunDamage','rainFadeIn','rainFadeOut','boltFadeIn',
            'boltFadeOut','boltFrequency','weatherType','boltRed','boltBlue','boltGreen'),
        MelStructs('SNAM','2I','sounds',(FID,'sound'),'type'),
        )
    __slots__ = MelRecord.__slots__ + melSet.getSlotsUsed()

#------------------------------------------------------------------------------
# These Are normally not mergable but added to brec.MreRecord.type_class
#
#       MreCell,
#------------------------------------------------------------------------------
# These have undefined FormIDs Do not merge them
#
#
#------------------------------------------------------------------------------
# These need syntax revision but can be merged once that is corrected
#
#
#------------------------------------------------------------------------------
#--Mergeable record types

# Old Mergable from Valda's version
# MreActi, MreAlch, MreAloc, MreAmef, MreAmmo, MreAnio, MreAppa, MreArma, MreArmo, MreAspc, MreAvif,
# MreBook, MreBptd, MreBsgn, MreCcrd, MreCdck, MreChal, MreChip, MreClas, MreClmt, MreClot, MreCmny,
# MreCont, MreCrea, MreCsno, MreCsty, MreDebr, MreDehy, MreDobj, MreDoor, MreEczn, MreEfsh, MreEnch,
# MreExpl, MreEyes, MreFact, MreFlor, MreFlst, MreFurn, MreGlob, MreGras, MreHair, MreHdpt, MreHung,
# MreIdle, MreIdlm, MreImad, MreImod, MreIngr, MreIpct, MreIpds, MreKeym, MreLigh, MreLscr, MreLsct,
# MreLtex, MreLvlc, MreLvli, MreLvln, MreLvsp, MreMgef, MreMicn, MreMisc, MreMset, MreMstt, MreMusc,
# MreNote, MreNpc, MrePack, MrePerk, MreProj, MrePwat, MreQust, MreRace, MreRcct, MreRcpe, MreRegn,
# MreRepu, MreSbsp, MreScpt, MreSgst, MreSkil, MreSlgm, MreSlpd, MreSoun, MreSpel, MreStat, MreTact,
# MreTerm, MreTree, MreTxst, MreVtyp, MreWatr, MreWeap, MreWthr,

mergeClasses = (
        # MreAchr, MreAcre, MreGmst, MrePgre,
        MreActi, MreAddn, MreAlch, MreAloc, MreAmef, MreAmmo, MreAnio, MreArma, MreArmo, MreAspc,
        MreAvif, MreBook, MreBptd, MreCams, MreCcrd, MreCdck, MreChal, MreChip, MreClas, MreClmt,
        MreCmny, MreCobj, MreCont, MreCpth, MreCrea, MreCsno, MreCsty, MreDebr, MreDehy, MreDobj,
        MreDoor, MreEczn, MreEfsh, MreEnch, MreExpl, MreEyes, MreFact, MreFlst, MreFurn, MreGlob,
        MreGras, MreHair, MreHdpt, MreHung, MreIdle, MreIdlm, MreImad, MreImgs, MreImod, MreIngr,
        MreIpct, MreIpds, MreKeym, MreLgtm, MreLigh, MreLscr, MreLsct, MreLtex, MreLvlc, MreLvli,
        MreLvln, MreMesg, MreMgef, MreMicn, MreMisc, MreMset, MreMstt, MreMusc, MreNote, MreNpc,
        MrePack, MrePerk, MreProj, MrePwat, MreQust, MreRace, MreRads, MreRcct, MreRcpe, MreRegn,
        MreRepu, MreRgdl, MreScol, MreScpt, MreSlpd, MreSoun, MreSpel, MreStat, MreTact, MreTerm,
        MreTree, MreTxst, MreVtyp, MreWatr, MreWeap, MreWthr,
    )

#--Extra read classes: these record types will always be loaded, even if patchers
#  don't need them directly (for example, for MGEF info)
readClasses = ()
writeClasses = ()

def init():
    # Due to a bug with py2exe, 'reload' doesn't function properly.  Instead of
    # re-executing all lines within the module, it acts like another 'import'
    # statement - in otherwords, nothing happens.  This means any lines that
    # affect outside modules must do so within this function, which will be
    # called instead of 'reload'

# From Valda's version
# MreAchr, MreAcre, MreActi, MreAlch, MreAloc, MreAmef, MreAmmo, MreAnio, MreAppa, MreArma,
# MreArmo, MreAspc, MreAvif, MreBook, MreBptd, MreBsgn, MreCcrd, MreCdck, MreChal,
# MreChip, MreClas, MreClmt, MreClot, MreCmny, MreCont, MreCrea, MreCsno, MreCsty, MreDebr,
# MreDehy, MreDial, MreDobj, MreDoor, MreEczn, MreEfsh, MreEnch, MreExpl, MreEyes, MreFact,
# MreFlor, MreFlst, MreFurn, MreGlob, MreGmst, MreGras, MreHair, MreHdpt, MreHung, MreIdle,
# MreIdlm, MreImad, MreImod, MreInfo, MreIngr, MreIpct, MreIpds, MreKeym, MreLigh, MreLscr,
# MreLsct, MreLtex, MreLvlc, MreLvli, MreLvln, MreLvsp, MreMgef, MreMicn, MreMisc, MreMset,
# MreMstt, MreMusc, MreNote, MreNpc, MrePack, MrePerk, MreProj, MrePwat, MreQust,
# MreRace, MreRcct, MreRcpe, MreRefr, MreRegn, MreRepu, MreRoad, MreSbsp, MreScpt, MreSgst,
# MreSkil, MreSlgm, MreSlpd, MreSoun, MreSpel, MreStat, MreTact, MreTerm, MreTes4, MreTree,
# MreTxst, MreVtyp, MreWatr, MreWeap, MreWthr,
# MreCell, MreWrld, MreNavm,

    brec.ModReader.recHeader = RecordHeader

    #--Record Types
    brec.MreRecord.type_class = dict((x.classType,x) for x in (

        # Verified
        MreAchr, MreAcre, MreDial, MreGmst, MreInfo, MrePgre, MrePmis, MreRefr,
        MreActi, MreAddn, MreAlch, MreAloc, MreAmef, MreAmmo, MreAnio, MreArma, MreArmo, MreAspc,
        MreAvif, MreBook, MreBptd, MreCams, MreCcrd, MreCdck, MreChal, MreChip, MreClas, MreClmt,
        MreCmny, MreCobj, MreCont, MreCpth, MreCrea, MreCsno, MreCsty, MreDebr, MreDehy, MreDobj,
        MreDoor, MreEczn, MreEfsh, MreEnch, MreExpl, MreEyes, MreFact, MreFlst, MreFurn, MreGlob,
        MreGras, MreHair, MreHdpt, MreHung, MreIdle, MreIdlm, MreImad, MreImgs, MreImod, MreIngr,
        MreIpct, MreIpds, MreKeym, MreLgtm, MreLigh, MreLscr, MreLsct, MreLtex, MreLvlc, MreLvli,
        MreLvln, MreMesg, MreMgef, MreMicn, MreMisc, MreMset, MreMstt, MreMusc, MreNote, MreNpc,
        MrePack, MrePerk, MreProj, MrePwat, MreQust, MreRace, MreRads, MreRcct, MreRcpe, MreRegn,
        MreRepu, MreRgdl, MreScol, MreScpt, MreSlpd, MreSoun, MreSpel, MreStat, MreTact, MreTerm,
        MreTree, MreTxst, MreVtyp, MreWatr, MreWeap, MreWthr,
        MreCell, MreNavm, MreNavi, MreWrld,
        MreHeader,
        ))
    #--Simple records
    brec.MreRecord.simpleTypes = (set(brec.MreRecord.type_class) -
        # set(('TES4','ACHR','ACRE','REFR','CELL','PGRD','ROAD','LAND','WRLD','INFO','DIAL','NAVM')))
        set((
        'TES4','ACHR','ACRE','CELL','DIAL','INFO','LAND','NAVI','NAVM','PGRE','PMIS','REFR','WRLD',
        )))
