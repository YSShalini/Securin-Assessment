import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_cves_basic():
    """Test CVE list API basic response"""
    response = client.get("/cves/list")
    assert response.status_code == 200

    body = response.json()
    assert "total" in body
    assert "data" in body
    assert isinstance(body["data"], list)


def test_list_cves_pagination():
    """Test pagination with limit & offset"""
    response = client.get("/cves/list?limit=5&offset=0")
    assert response.status_code == 200

    body = response.json()
    assert len(body["data"]) <= 5


def test_filter_by_year():
    """Test filtering CVEs by year"""
    response = client.get("/cves/list?year=1999&limit=5")
    assert response.status_code == 200

    body = response.json()
    for cve in body["data"]:
        assert cve["cve_id"].startswith("CVE-1999-")


def test_filter_by_score():
    """Test filtering CVEs by CVSS score"""
    response = client.get("/cves/list?score=7")
    assert response.status_code == 200


def test_filter_by_last_modified_days():
    """Test filtering by last modified days"""
    response = client.get("/cves/list?last_days=30")
    assert response.status_code == 200


def test_get_single_cve():
    """Test fetching a known CVE"""
    response = client.get("/cves/CVE-1999-1198")
    assert response.status_code == 200

    body = response.json()
    assert body["cve_id"] == "CVE-1999-1198"
    assert "description" in body


def test_get_invalid_cve():
    """Test invalid CVE returns 404"""
    response = client.get("/cves/CVE-0000-0000")
    assert response.status_code == 404
