# Swimlane Migrator
* Require's Swimlane python driver https://github.com/swimlane/swimlane-python
* Used in combination with Swimlane Migration Tool Watershed package

# Installation
```bash
pip install swimlane-migrator
```

# Change Log

## 0.4.2
* Fixed issue using asset as python script inputs

## 0.4.1
* Fixed issue handling email assets that don't have a version number

## 0.4.0
* Fixed issue causing tasks with no asset to raise error
* Cleaned up workspace management

## 0.3.0
* Email Assets are now properly migrated
* If a swimbundle is not found it will automatically be migrated

## 0.2.2
* Setup description to be displayed properly

## 0.2.1
* Fixed bug that threw error when integrations had an empty input

## 0.2.0
* Initial Release