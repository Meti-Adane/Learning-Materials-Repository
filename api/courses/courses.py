from api.models import Course
from api.admin.validate import validate_arg
from flask_restful import Resource
from flask import json, request, Response


class GetCourses(Resource):

    def get(self):
        search_query = request.args.get("search_query")
        
        if search_query:
            return Response(json.dumps(Course.search(search_query)), status=200)
        
        page = request.args.get("page")
        if page:
            page = int(page)
        else:
            page = 1
        
        limit = request.args.get("limit")
        if limit:
            limit = int(limit)
        else:
            limit = 10
        courses = Course.query.paginate(page=page, per_page=limit, error_out=False)
        all_courses = courses.items

        if len(all_courses) == 0:
            return Response(json.dumps({"Message": "No courses found"}), status=404)
        
        total_pages = courses.pages
        current_page = page

        return Response(json.dumps({"Courses": [book.serialize for book in all_courses], "totalPages": total_pages, "currentPage": current_page}), status=200)


class GetCourse(Resource):

    def get(self, course_id):

        if validate_arg(course_id):
            return validate_arg(course_id)

        course = Course.get_course_by_id(id=course_id)
        if not course:
            return Response(json.dumps({"Message": "Course does not exist"}), status=404)

        return Response(json.dumps(course.serialize),status = 200)  