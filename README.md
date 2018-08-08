# kanji-extractor
Automatically create kanji notes based on the kanji used in other notes.

# Planned Features

* Create kanji notes with the following information:
    * Kanji
    * Onyomi
    * Kunyomi
    * Meaning
    * kanji
    * Example words (found from users collection)
    * Example words with meaning
    * Radical
    * Stroke number
    * Tags: JLPT Level, Kanji Grade and tags set by user
* Use other notes of the Anki Collection as sources for the Kanji notes:
    * Multiple note types can be selected
    * On each note mutliple fields can be selected, which will be considered as sources
    * The fields can be selected as sources for example words and can be mapped to a meaning field
* Only notes in a selected scope are created
    * The Scope is defined by the JLPT Levels
    * The user can black list kanji characters, for which no notes will be created
* Note creation / updating:
    * Selected notes in the browser will be used for note creation
    * Normally only new notes will be considered for the creation process
    * Adding new notes, whose note type is selected as a source, example words will be appended to the kanji note
* UI Elements
    * UI for the settings
    * Action in the Tools section of Anki's main window
    * Action in the Edit section in the browser menu
