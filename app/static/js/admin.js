import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UpdateTeacherCourse() {
    const [teacherCourses, setTeacherCourses] = useState([]);
    const [selectedCourse, setSelectedCourse] = useState({});
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    useEffect(() => {
        axios.get('/get_teacher_courses')  // adjust this route to match your Flask endpoint
            .then(response => {
                setTeacherCourses(response.data);
                setSelectedCourse(response.data[0] || {});  // default to first course
            });
    }, []);

    const handleCourseChange = (e) => {
        const courseId = e.target.value;
        const selected = teacherCourses.find(tc => tc.id === courseId);
        setSelectedCourse(selected || {});
    };

    const handleUpdate = () => {
        axios.post('/update_teacher_course', {  // adjust this route and the data structure to match your Flask endpoint
            id: selectedCourse.id,
            start_date: startDate,
            end_date: endDate
        })
        .then(response => {
            // handle the response here, maybe refresh the courses list
        });
    };

    return (
        <div>
            <select value={selectedCourse.id} onChange={handleCourseChange}>
                {teacherCourses.map(tc => (
                    <option key={tc.id} value={tc.id}>{tc.course_name}</option>
                ))}
            </select>
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
            <button onClick={handleUpdate}>Update</button>
        </div>
    );
}

export default UpdateTeacherCourse;