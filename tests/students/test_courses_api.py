import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def course():
    return Course.objects.create(name='1')


@pytest.fixture()
def course_factory():
    def factory(*args,**kwargs):
        return baker.make(Course,*args,**kwargs)

    return factory


@pytest.mark.django_db
def test_first_course(client,course):
    response = client.get(f'/courses/?name={course.name}')
    assert response.json()[0]['name'] == course.name


@pytest.mark.django_db
def test_list_course(client,course_factory):
    courses_name = course_factory(_quantity=10)
    response = client.get('/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses_name)
    for i, course in enumerate(data):
        assert course['name'] == courses_name[i].name


@pytest.mark.django_db
def test_filter_course_id(client,course_factory):
    courses_id = course_factory(_quantity=10)
    print(type(courses_id))
    response = client.get(f'/courses/?id={courses_id[0].id}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses_id[0].id



@pytest.mark.django_db
def test_filter_course_name(client,course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/courses/?name={courses[0].name}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_create_course(client):
    response = client.post('/courses/',
                           data={'name': '1'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_course(client, course):
    response = client.patch(f'/courses/{course.id}/',
                            data={'name': '2'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == '2'


@pytest.mark.django_db
def test_delete_course(client, course):
    response = client.delete(f'/courses/{course.id}/')
    assert response.status_code == 204
