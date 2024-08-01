"""
This module defines classes that encapsulate configurations and rewards for various game queues
in the League of Legends gaming environment, based on data from the /lol-game-queues/v1/queues/{id} API endpoint.
These classes organize complex game queue settings and reward structures into accessible and manageable properties.

Usage:
    These classes are utilized primarily to provide structured access to game queue data. This organization assists
    developers in implementing features that interact with, modify, or display game queue settings within the League of
    Legends client or associated tools. The classes ensure data integrity and provide a clear interface for
    working with the complex data returned by the game's API.
"""


class LolGameQueuesQueueGameTypeConfig:
    """Manages game type configurations, including rules for picking, banning,
    and match setup parameters specific to each queue.
    """

    ADVANCED_LEARNING_QUESTS = "advancedLearningQuests"
    ALLOW_TRADES = "allowTrades"
    BAN_MODE = "banMode"
    BAN_TIMER_DURATION = "banTimerDuration"
    BATTLE_BOOST = "battleBoost"
    CROSS_TEAM_CHAMPION_POOL = "crossTeamChampionPool"
    DEATH_MATCH = "deathMatch"
    DO_NOT_REMOVE = "doNotRemove"
    DUPLICATE_PICK = "duplicatePick"
    EXCLUSIVE_PICK = "exclusivePick"
    GAME_MODE_OVERRIDE = "gameModeOverride"
    ID = "id"
    LEARNING_QUESTS = "learningQuests"
    MAIN_PICK_TIMER_DURATION = "mainPickTimerDuration"
    MAX_ALLOWABLE_BANS = "maxAllowableBans"
    NAME = "name"
    NUM_PLAYERS_PER_TEAM_OVERRIDE = "numPlayersPerTeamOverride"
    ONBOARD_COOP_BEGINNER = "onboardCoopBeginner"
    PICK_MODE = "pickMode"
    POST_PICK_TIMER_DURATION = "postPickTimerDuration"
    REROLL = "reroll"
    TEAM_CHAMPION_POOL = "teamChampionPool"


class LolGameQueuesQueueReward:
    """Details the reward configurations available per game queue, such as XP and IP earnings."""

    IS_CHAMPION_POINTS_ENABLED = "isChampionPointsEnabled"
    IS_IP_ENABLED = "isIpEnabled"
    IS_XP_ENABLED = "isXpEnabled"
    PARTY_SIZE_IP_REWARDS = "partySizeIpRewards"


class LolGameQueuesQueue:
    """Represents the main structure of a game queue, including its operational parameters,
    such as team settings, champion requirements, and queue availability.
    """

    ALLOWABLE_PREMADE_SIZES = "allowablePremadeSizes"
    ARE_FREE_CHAMPIONS_ALLOWED = "areFreeChampionsAllowed"
    ASSET_MUTATOR = "assetMutator"
    CATEGORY = "category"
    CHAMPIONS_REQUIRED_TO_PLAY = "championsRequiredToPlay"
    DESCRIPTION = "description"
    DETAILED_DESCRIPTION = "detailedDescription"
    GAME_MODE = "gameMode"
    GAME_TYPE_CONFIG = "gameTypeConfig"
    ID = "id"
    IS_RANKED = "isRanked"
    IS_TEAM_BUILDER_MANAGED = "isTeamBuilderManaged"
    IS_TEAM_ONLY = "isTeamOnly"
    LAST_TOGGLED_OFF_TIME = "lastToggledOffTime"
    LAST_TOGGLED_ON_TIME = "lastToggledOnTime"
    MAP_ID = "mapId"
    MAX_DIVISION_FOR_PREMADE_SIZE2 = "maxDivisionForPremadeSize2"
    MAX_LEVEL = "maxLevel"
    MAX_SUMMONER_LEVEL_FOR_FIRST_WIN_OF_THE_DAY = "maxSummonerLevelForFirstWinOfTheDay"
    MAX_TIER_FOR_PREMADE_SIZE2 = "maxTierForPremadeSize2"
    MAXIMUM_PARTICIPANT_LIST_SIZE = "maximumParticipantListSize"
    MIN_LEVEL = "minLevel"
    MINIMUM_PARTICIPANT_LIST_SIZE = "minimumParticipantListSize"
    NAME = "name"
    NUM_PLAYERS_PER_TEAM = "numPlayersPerTeam"
    QUEUE_AVAILABILITY = "queueAvailability"
    QUEUE_REWARDS = "queueRewards"
    REMOVAL_FROM_GAME_ALLOWED = "removalFromGameAllowed"
    REMOVAL_FROM_GAME_DELAY_MINUTES = "removalFromGameDelayMinutes"
    SHORT_NAME = "shortName"
    SHOW_POSITION_SELECTOR = "showPositionSelector"
    SPECTATOR_ENABLED = "spectatorEnabled"
    TYPE = "type"
