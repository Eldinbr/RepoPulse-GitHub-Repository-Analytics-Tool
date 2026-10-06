from repopulse.metrics import calculate_change, extract_metrics, percentage_change


def test_extract_metrics():
    data = {
        "stargazers_count": 100,
        "forks_count": 20,
        "open_issues_count": 5,
        "watchers_count": 90,
        "size": 1234,
        "language": "Python",
    }
    assert extract_metrics(data) == {
        "stars": 100,
        "forks": 20,
        "open_issues": 5,
        "watchers": 90,
        "size_kb": 1234,
        "language": "Python",
    }


def test_change():
    assert calculate_change(120, 100) == 20
    assert calculate_change(120, None) == 120


def test_percentage_change():
    assert percentage_change(120, 100) == 20.0
    assert percentage_change(100, 0) is None
