from datetime import datetime

from rest_framework import serializers

from schedules.models import Classroom, Schedule


def format_code(codes):
    morning = ['07:00', '07:55', '08:50', '10:10', '11:05']
    afternoon = ['13:30', '14:25', '15:45', '16:40', '17:35']
    night = ['19:00', '19:50', '21:00', '22:40', '22:40']

    formatted_codes = []

    for code in codes:
        formatted_code = str(code).split(' ')

        for cod in formatted_code:
            code_weekday = cod[0]
            # if True:
            print(code_weekday, datetime.now().weekday()+2)
            if int(code_weekday) == datetime.now().weekday()+2:
                code_semester = cod[1]
                hour_start = int(cod[2]) - 1
                formatted_hour = ''

                if code_semester.upper() == 'T':
                    horario_formatado = afternoon[hour_start]
                    formatted_hour = horario_formatado + ':00'

                if code_semester.upper() == 'M':
                    horario_formatado = morning[hour_start]
                    formatted_hour = horario_formatado + ':00'

                if code_semester.upper() == 'N':
                    horario_formatado = night[hour_start]
                    formatted_hour = horario_formatado + ':00'

                formatted_codes.append(formatted_hour)

    # for code in formatted_codes:
    #     print(code)
    return formatted_codes


class ClassroomSpecialSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField()

    def get_schedules(self, obj: Classroom):
        return format_code(obj.content['schedules'])

    class Meta:
        model = Classroom
        exclude = ['content', 'id', 'profile']
        read_only_fields = ['id']
        depth = 1


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'
        read_only_fields = ['id']
        depth = 1


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['id']
        depth = 1