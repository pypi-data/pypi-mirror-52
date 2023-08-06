# Imports from python.
from datetime import datetime


# Imports from other dependencies.
from election.models import Candidate
from election.models import CandidateElection
from election.models import Election
from election.models import ElectionCycle
from election.models import ElectionDay
from election.models import ElectionType
from election.models import Race
from entity.models import Person


# Imports from election_loader.
from election_loader.utils.lookups.geography import get_state_division
from election_loader.utils.lookups.geography import get_district_division
from election_loader.utils.lookups.government import get_governor_office
from election_loader.utils.lookups.government import get_house_office
from election_loader.utils.lookups.government import get_party
from election_loader.utils.lookups.government import get_senate_office


ELECTION_TYPE_MAP = dict(ElectionType.TYPES)

ELECTION_TYPE_ARGS_BY_RACE_TYPE = {
    "General": dict(
        slug=ElectionType.GENERAL,
        label=ELECTION_TYPE_MAP[ElectionType.GENERAL],
    ),
    "Special General": dict(
        slug=ElectionType.GENERAL,
        label=ELECTION_TYPE_MAP[ElectionType.GENERAL],
    ),
    "Primary": dict(
        slug=ElectionType.PARTY_PRIMARY,
        label=ELECTION_TYPE_MAP[ElectionType.PARTY_PRIMARY],
    ),
    "Open Primary": dict(
        slug=ElectionType.JUNGLE_PRIMARY,
        label=ELECTION_TYPE_MAP[ElectionType.JUNGLE_PRIMARY],
    ),
    # "TK": dict(
    #     slug=ElectionType.PRIMARY_RUNOFF,
    #     label=ELECTION_TYPE_MAP[ElectionType.PRIMARY_RUNOFF],
    # ),
    # "TK": dict(
    #     slug=ElectionType.GENERAL_RUNOFF,
    #     label=ELECTION_TYPE_MAP[ElectionType.GENERAL_RUNOFF],
    # ),
}


def create_election_cycle(race):
    year = race["electiondate"][:4]
    cycle, created = ElectionCycle.objects.get_or_create(name=year)
    return cycle


def create_election_day(race):
    date = datetime.strptime(race["electiondate"], "%Y-%m-%d")
    cycle = create_election_cycle(race)
    day, created = ElectionDay.objects.get_or_create(cycle=cycle, date=date)
    return day


def create_race(race):
    election_day = create_election_day(race)
    cycle = election_day.cycle
    if race["officeid"] == "H":
        office = get_house_office(
            state_id=race["statepostal"], seat_num=race["seatnum"].zfill(2)
        )
    elif race["officeid"] == "S":
        office = get_senate_office(
            state_id=race["statepostal"], senate_class=race["description"]
        )
    elif race["officeid"] == "G":
        office = get_governor_office(state_id=race["statepostal"])
    race, created = Race.objects.get_or_create(
        office=office,
        cycle=cycle,
        special=race["seatname"] == "Unexpired Term"
        or "Special" in race["racetype"],
    )
    return race


def create_election_type(race):
    # This should really be a mgmt command creating fixtures on
    # the civic-election with a lookup in utils...

    election_type, created = ElectionType.objects.get_or_create(
        **ELECTION_TYPE_ARGS_BY_RACE_TYPE[race["racetype"]]
    )

    # if race["racetypeid"] == "G":
    #     election_type, created = ElectionType.objects.get_or_create(
    #         slug=ElectionType.GENERAL, label="General"
    #     )
    # if race["racetypeid"] == "R":
    #     election_type, created = ElectionType.objects.get_or_create(
    #         slug=ElectionType.PARTY_PRIMARY, label="Party Primary"
    #     )

    # TODO: All the others...
    # - Jungle Primary
    # - General runoff
    # - Party primary runoff
    return election_type


def create_person(race):
    person, created = Person.objects.get_or_create(
        first_name=race["first"],
        last_name=race["last"],
        identifiers={"ap_polid": race["polid"]},
    )
    return person


def create_candidate(race):
    candidate, created = Candidate.objects.get_or_create(
        race=create_race(race),
        person=create_person(race),
        party=get_party(race["party"]),
        ap_candidate_id="polnum-{}".format(race["polnum"]),
        incumbent=race["incumbent"],
    )

    return candidate


def create_election(race):
    # For primaries, affiliate a primary with a party
    if race["racetype"] == "Primary":
        party = get_party(race["party"])
    else:
        party = None

    if race["officeid"] == "H":
        division = get_district_division(
            race["statepostal"], race["seatnum"].zfill(2)
        )
    else:
        division = get_state_division(race["statepostal"])

    election, created = Election.objects.get_or_create(
        election_type=create_election_type(race),
        race=create_race(race),
        party=party,
        election_day=create_election_day(race),
        division=division,
        ap_election_id=race["raceid"],
    )

    return election


def create_candidate_election(race):
    party = get_party(race["party"])
    candidate_election, created = CandidateElection.objects.get_or_create(
        candidate=create_candidate(race),
        election=create_election(race),
        uncontested=race["uncontested"],
        aggregable=party.aggregate_candidates,
    )

    return candidate_election
