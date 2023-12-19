from datetime import datetime

from .serializers import *
from Automac_machines_app.models import Machine_KPI_Data,MachineDetails

from Automac_machines_app.serializers import machineSerializer

def kpi_data_to_database(instance):
    # print('instance',instance)
    # print('type  instance',type(instance))
    machine_id = instance.machine_id
    time_stamp = instance.timestamp
    today = datetime.now().date()

    machine_data = all_Machine_data.objects.filter(machine_id__machine_id=machine_id)

    for data in machine_data:
        data_kpi = data.kpi
        # print('data_kpi',data_kpi)
        if data_kpi is not None and data_kpi.kpi_inventory_id.Kpi_Type == "Energy_Card":
            datapoints = data_kpi.data_points[0]
            # print('datapoints',datapoints)
            kpiname = data_kpi.kpi_name
            kpi_data = eval(f'instance.{datapoints}')  # Assuming instance.points is accessible
            # kpi_data = getattr(instance,datapoints)  # Assuming instance.points is accessible
            # kpi_data = instance.datapoints  # Assuming instance.points is accessible
            # print('..................................',datapoints,'??????????',kpiname,'///////',kpi_data)
            kpi_data_queryset = Machine_KPI_Data.objects.filter(machine_id=machine_id, kpi_id__kpi_name=kpiname, timestamp__date=today)
            print('kpi_data_queryset',kpi_data_queryset)
            if kpi_data_queryset.exists():
                print('exitssssssssss')
                # Update the existing record(s) for cumulative data
                kpi_data_queryset.update(kpi_data=kpi_data, timestamp=time_stamp)
            else:
                # print('createeeeeeeeeee')
                Machine_KPI_Data.objects.create(
                    machine_id=machine_id,
                    kpi_id=data_kpi,
                    kpi_data=kpi_data,
                    timestamp=time_stamp
                )
        if data_kpi is not None and data_kpi.kpi_inventory_id.Kpi_Type == "Text_Card":
            print('Text_Card')
            datapoints = data_kpi.data_points[0]
            # print('datapoints', datapoints)
            kpiname = data_kpi.kpi_name
            # kpi_data = getattr(instance,datapoints)
            kpi_data = eval(f'instance.{datapoints}')
            # print('..................................',datapoints,'??????????',kpiname,'///////',kpi_data)



            kpi_data_queryset = Machine_KPI_Data.objects.filter(machine_id=machine_id, kpi_id__kpi_name=kpiname,
                                                                timestamp__date=today)
            # print('kpi_data_queryset', kpi_data_queryset)

            if kpi_data_queryset.exists():
                # Update the existing record(s) for cumulative data
                kpi_data_queryset.update(kpi_data=[str(kpi_data)], timestamp=time_stamp)
            else:
                # Create a new record for cumulative data if it doesn't exist
                Machine_KPI_Data.objects.create(
                    machine_id=machine_id,
                    kpi_id=data.kpi,
                    kpi_data=[str(kpi_data)],
                    timestamp=time_stamp
                )
        if data_kpi is not None and data_kpi.kpi_inventory_id.Kpi_Type == "Line_Graph":
            # print('Line_Graph')
            datapoints = data_kpi.data_points[0]
            # print('datapoints', datapoints)
            kpiname = data_kpi.kpi_name
            kpi_data = eval(f'instance.{datapoints}')
            # kpi_data = getattr(instance, datapoints)
            # print('..................................', datapoints, '??????????', kpiname, '///////', kpi_data)


            Machine_KPI_Data.objects.create(
                machine_id=machine_id,
                kpi_id=data.kpi,
                kpi_data=[str(kpi_data)],
                timestamp=time_stamp
            )

        if data_kpi is not None and data_kpi.kpi_inventory_id.Kpi_Type == "production_difference":
            # print('production_difference')
            datapoints = data_kpi.data_points[0]#split coulumn_name and  value
            # print('datapoints', datapoints)
            kpiname = data_kpi.kpi_name
            # print('kpiname',kpiname)
            datapoints_split=datapoints.split('[')
            col=datapoints_split[0]
            index=int(datapoints_split[1][:-1])
            # print('.........','col',col,'\\\\','index',index)

            # kpi_data = getattr(instance,datapoints)
            kpi_data = eval(f'instance.{datapoints}')
            # print('kpidata',kpi_data)

            # print('..................................',datapoints,'??????????',kpiname,'///////',kpi_data)
            first_record = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=today).earliest(
                'timestamp')
            latest_record = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=today).latest(
                'timestamp')


            print('first_record',first_record)
            # print('type',type(first_record))
            # print('type',dir(first_record))

            # # print('first_record',first_record.eval(f'instance.{datapoints}'))
            # latest_record=first_value.latest()
            print('latest_record',latest_record)

            # first_record_data=first_record+"."f"{datapoints}"
            first_record_data = getattr(first_record, f"{col}")[index]
            # first_record_data=first_record.other[7]
            print('first_record_data',first_record_data)
            print('first_type',type(first_record_data))

            last_record_data=latest_record.other[7]
            # print('last_record_data',last_record_data)
            # print('last_type',type(last_record_data))


            result_data=int(float(last_record_data)) - int(float(first_record_data))
            print('result_data',result_data)

            kpi_data_queryset = Machine_KPI_Data.objects.filter(machine_id=machine_id, kpi_id__kpi_name=kpiname,
                                                                timestamp__date=today)
            # print('kpi_data_queryset', kpi_data_queryset)
            # print('counttt', kpi_data_queryset.count())

            if kpi_data_queryset.exists():
                # Update the existing record(s) for cumulative data
                kpi_data_queryset.update(kpi_data=[str(result_data)], timestamp=time_stamp)
            else:
                # Create a new record for cumulative data if it doesn't exist
                Machine_KPI_Data.objects.create(
                    machine_id=machine_id,
                    kpi_id=data.kpi,
                    kpi_data=[str(result_data)],
                    timestamp=time_stamp
                )

        if data_kpi is not None and data_kpi.kpi_inventory_id.Kpi_Type == "Min_Max_values":
            print('Min_Max_values')
            datapoints = data_kpi.data_points[0]#split coulumn_name and  value
            # print('datapoints', datapoints)
            kpiname = data_kpi.kpi_name
            # print('kpiname',kpiname)
            datapoints_split=datapoints.split('[')
            col=datapoints_split[0]
            index=int(datapoints_split[1][:-1])
            print('.........','col',col,'\\\\','index',index)

            # kpi_data = getattr(instance,datapoints)
            # kpi_data = eval(f'instance.{datapoints}')
            # print('kpidata',kpi_data)

            # print('..................................',datapoints,'??????????',kpiname,'///////',kpi_data)
            first_record = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=today).latest(
                'timestamp')

            min_max_data_query = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=today)
            print('min_max_data_query',min_max_data_query)
            lowest = getattr(first_record, f"{col}")[index]
            print('lowest',lowest)
            highest = getattr(first_record, f"{col}")[index]
            print('highest',highest)
            min_max_data_query = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=today)


            for m in range(len(min_max_data_query)):
                # print('mmmmmmmmmmmmm',m)
                print('indexxx',index)
                record_data = getattr(min_max_data_query[m], f"{col}")
                record_data = record_data[index]
                # record_data = getattr(min_max_data_query[m], f"{col}")[index]
                print('record_data',record_data)
                if record_data > highest:
                    highest = record_data
                elif record_data < lowest:
                    lowest = record_data

                # print('min ',str(lowest), "max",str(highest))
                high_low_result=[lowest,highest]
                # print('high_low_result',high_low_result)

            kpi_data_queryset = Machine_KPI_Data.objects.filter(machine_id=machine_id, kpi_id__kpi_name=kpiname,
                                                                timestamp__date=today)
            # print('kpi_data_queryset', kpi_data_queryset)
            # print('kpiname', kpiname)


            # print('counttt', kpi_data_queryset.count())#10517

            if kpi_data_queryset.exists():
                # Update the existing record(s) for cumulative data
                kpi_data_queryset.update(kpi_data=high_low_result, timestamp=time_stamp)
            else:
                # Create a new record for cumulative data if it doesn't exist
                Machine_KPI_Data.objects.create(
                    machine_id=machine_id,
                    kpi_id=data.kpi,
                    kpi_data=high_low_result,
                    timestamp=time_stamp
                )

