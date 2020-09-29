from database import Database
import json

def test1():
    # Initial graph
    build = [("core", None), ("A", "core"), ("B", "core"), ("C", "core"), ("C1", "C")]
    # Extract
    extract = {"img001": ["A", "B"], "img002": ["A", "C1"], "img003": ["B", "E"]}
    # Graph edits
    edits = [("A1", "A"), ("A2", "A"), ("C2", "C")]

    # Get status (this is only an example, test your code as you please as long as it works)
    status = {}
    if len(build) > 0:
        # Build graph
        db = Database(build[0][0])
        if len(build) > 1:
            db.add_nodes(build[1:])
        # Add extract
        db.add_extract(extract)
        # Graph edits
        db.add_nodes(edits)
        # Update status
        status = db.get_extract_status()
        assert status == {'img001': 'granularity_staged', 'img002': 'coverage_staged', 'img003': 'invalid'}


def test2():
    # Initial graph
    build = [("core", None), ("A", "core"), ("B", "core"), ("C", "core"), ("C1", "C")]
    # Extract
    extract = {"img001": ["A"], "img002": ["C1"]}
    # Graph edits
    edits = [("A1", "A"), ("A2", "A")]

    # Get status (this is only an example, test your code as you please as long as it works)
    status = {}
    if len(build) > 0:
        # Build graph
        db = Database(build[0][0])
        if len(build) > 1:
            db.add_nodes(build[1:])
        # Add extract
        db.add_extract(extract)
        # Graph edits
        db.add_nodes(edits)
        # Update status
        status = db.get_extract_status()
    assert status == {"img001": "granularity_staged", "img002": "valid"}

def test3():
    # Initial graph
    with open('graph_build.json') as f:
        build = json.load(f)
    # Extract
    with open('img_extract.json') as f:
        extract = json.load(f)
    # Graph edits
    with open('graph_edits.json') as f:
        edits = json.load(f)
    # Expected_status
    with open('expected_status.json') as f:
        expected_status = json.load(f)

    # Get status (this is only an example, test your code as you please as long as it works)
    status = {}
    if len(build) > 0:
        # Build graph
        db = Database(build[0][0])
        if len(build) > 1:
            db.add_nodes(build[1:])
        # Add extract
        db.add_extract(extract)
        # Graph edits
        db.add_nodes(edits)
        # Update status
        status = db.get_extract_status()
    assert status == expected_status

if __name__=='__main__':
    test1()
    test2()
    test3()
