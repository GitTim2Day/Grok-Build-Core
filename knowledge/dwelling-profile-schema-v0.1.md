# Dwelling Profile Schema — v0.1 (adapted from QuoteBot)

**Date:** 2026-09-03
**Source:** anakai3/insurance-quotebot profile-schema.json (MIT) + ACORD 84 (2026) + 2017 form gaps
**Status:** Draft. JSON Schema skeleton for a home/dwelling intake that an AI agent can consume.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Dwelling Insurance Quote Profile",
  "description": "Home/dwelling profile for AI-agent quote automation. Excludes SSN — agent prompts user to enter manually.",
  "type": "object",
  "properties": {
    "meta": {
      "type": "object",
      "properties": {
        "version": { "type": "string", "default": "0.1.0" },
        "createdAt": { "type": "string", "format": "date-time" },
        "updatedAt": { "type": "string", "format": "date-time" }
      }
    },
    "personalInfo": {
      "type": "object",
      "properties": {
        "firstName": { "type": "string" },
        "lastName": { "type": "string" },
        "dateOfBirth": { "type": "string", "format": "date" },
        "maritalStatus": { "type": "string", "enum": ["Single", "Married", "Domestic Partner", "Divorced", "Separated", "Widowed"] },
        "email": { "type": "string", "format": "email" },
        "phoneNumber": { "type": "string" }
      },
      "required": ["firstName", "lastName", "email", "phoneNumber"]
    },
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" },
        "zipCode": { "type": "string" },
        "county": { "type": "string" },
        "residenceType": { "type": "string", "enum": ["Primary", "Secondary", "Rental", "Vacant"] },
        "monthsAtAddress": { "type": "integer", "minimum": 0 }
      },
      "required": ["street", "city", "state", "zipCode"]
    },
    "property": {
      "type": "object",
      "description": "Replaces vehicles[] from QuoteBot",
      "properties": {
        "yearBuilt": { "type": "integer" },
        "constructionType": { "type": "string", "enum": ["Brick", "Frame", "Stucco", "Masonry Veneer", "Other"] },
        "stories": { "type": "integer" },
        "livingSqFt": { "type": "integer" },
        "totalSqFt": { "type": "integer" },
        "foundation": { "type": "string", "enum": ["Slab", "Crawl", "Basement", "Finished Basement"] },
        "basementFinishedSqFt": { "type": "integer" },
        "garage": { "type": "string", "enum": ["None", "Attached", "Detached", "Drive-under"] },
        "garageCars": { "type": "integer" },
        "fireplace": { "type": "string", "enum": ["None", "Insert", "Masonry"] },
        "gasLogs": { "type": "boolean" },
        "bathsFull": { "type": "integer" },
        "bathsHalf": { "type": "integer" }
      },
      "required": ["yearBuilt", "constructionType", "stories", "livingSqFt"]
    },
    "systems": {
      "type": "object",
      "properties": {
        "roofInstallYear": { "type": "integer" },
        "roofMaterial": { "type": "string" },
        "roofCondition": { "type": "string", "enum": ["Excellent", "Good", "Fair", "Poor"] },
        "roofPhotoRequired": { "type": "boolean", "default": true },
        "plumbingYear": { "type": "integer" },
        "wiringYear": { "type": "integer" },
        "hvacYear": { "type": "integer" },
        "electricalPanelAge": { "type": "integer" },
        "electricalPanelAmps": { "type": "integer" },
        "waterHeaterAge": { "type": "integer" },
        "centralHeat": { "type": "boolean" },
        "centralAir": { "type": "boolean" }
      }
    },
    "protection": {
      "type": "object",
      "properties": {
        "fireDeptName": { "type": "string" },
        "fireDeptDistanceMiles": { "type": "number" },
        "hydrantWithin1000ft": { "type": "boolean" },
        "smokeDetectors": { "type": "integer" },
        "fireExtinguishers": { "type": "integer" },
        "deadbolts": { "type": "boolean" },
        "alarmType": { "type": "string", "enum": ["None", "Local", "Central", "Monitored"] },
        "floodZone": { "type": "string" },
        "wildfireRisk": { "type": "string" }
      }
    },
    "hazards": {
      "type": "object",
      "properties": {
        "pool": { "type": "boolean" },
        "poolLiabilityLimit": { "type": "string" },
        "trampoline": { "type": "boolean" },
        "dogs": { "type": "boolean" },
        "dogBreeds": { "type": "array", "items": { "type": "string" } },
        "dogCount": { "type": "integer" },
        "fence": { "type": "boolean" },
        "fuelTanks": { "type": "boolean" },
        "businessUse": { "type": "boolean" }
      }
    },
    "claimsHistory": {
      "type": "array",
      "description": "Replaces drivingHistory from QuoteBot",
      "items": {
        "type": "object",
        "properties": {
          "date": { "type": "string", "format": "date" },
          "type": { "type": "string" },
          "amount": { "type": "number" },
          "description": { "type": "string" }
        }
      }
    },
    "scheduledItems": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "category": { "type": "string", "enum": ["Guns", "Jewelry", "Silver", "Electronics", "Musical Instruments", "Other"] },
          "limit": { "type": "number" }
        }
      }
    },
    "currentInsurance": {
      "type": "object",
      "properties": {
        "currentlyInsured": { "type": "boolean" },
        "currentCarrier": { "type": "string" },
        "policyNumber": { "type": "string" },
        "policyExpirationDate": { "type": "string", "format": "date" },
        "yearsContinuousCoverage": { "type": "number" },
        "reasonForSwitching": { "type": "string" }
      }
    },
    "coveragePreferences": {
      "type": "object",
      "properties": {
        "dwellingLimit": { "type": "number" },
        "personalPropertyLimit": { "type": "number" },
        "liabilityLimit": { "type": "string" },
        "deductible": { "type": "string", "enum": ["500", "1000", "2500", "5000"] },
        "replacementCostDwelling": { "type": "boolean" },
        "replacementCostContents": { "type": "boolean" },
        "ordinanceOrLaw": { "type": "boolean" },
        "waterBackup": { "type": "boolean" }
      }
    },
    "mortgagee": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "address": { "type": "string" },
        "loanNumber": { "type": "string" }
      }
    },
    "discounts": {
      "type": "object",
      "properties": {
        "multiPolicy": { "type": "boolean" },
        "paperless": { "type": "boolean" },
        "autopay": { "type": "boolean" },
        "homeSecurity": { "type": "boolean" },
        "newHomeDiscount": { "type": "boolean" }
      }
    },
    "agentInstructions": {
      "type": "object",
      "properties": {
        "sensitiveFieldBehavior": { "type": "string", "default": "STOP and ask user to enter SSN, credit card, or bank info manually" },
        "unknownFieldBehavior": { "type": "string", "default": "STOP and ask user" },
        "photoRequirement": { "type": "string", "default": "Require date-stamped roof and equipment photos before submit" }
      }
    }
  },
  "required": ["personalInfo", "address", "property", "systems", "protection", "currentInsurance", "coveragePreferences"]
}
```

## Mapping notes
- `property` replaces `vehicles[]`.
- `claimsHistory` replaces `drivingHistory`.
- `systems`, `protection`, `hazards`, `scheduledItems`, `mortgagee` are new.
- Conditional: pool yes → open poolLiabilityLimit + dogBreeds; roofCondition Poor → require photo + surcharge flag.
- Keep agentInstructions no-SSN rule from QuoteBot.
