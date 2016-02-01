# -*- coding: utf-8 -*-
import re, yaml, logging, inspect, math
import dropboxm
import calc_tools as ct
logger = logging.getLogger(__name__)

def calc(params_dict):
    globals().update(params_dict)  # very dirty!! polutes namespace

    logger.info("params_dict['flagThermo']\n%s" % (params_dict['flagThermo'],))
    logger.info("params_dict['flagFrLoss']\n%s" % (params_dict['flagFrLoss'],))

    flagB = flagTracker # контролируются ли левые ходки
    calc_results_dict = {}
    # i =ЕСЛИ(flagI;0;accu)
    i = 0. if flagI else accu # коэфф-т простоев !!! нигде не использвется! ввести.
    # b =ЕСЛИ(ИЛИ(flagPP;flagB);0;accu)
    if flag_passengers:
        b =  0. if flagPP else accu # коэфф-т "левых" пассажироперевозок
    else:
        b =  0. if flagB else accu # коэфф-т "левых" ходок
    # флаги берутся из params_dict


# Базовые величины для расчетов
    workout_cost_per_km = cost_loss_by_car_sell/prob # просто из головы. Ниакой оптимизации пока
    C0 = cost_loss_by_car_sell/x_k # себестоимость машины
    workout_in_hours = prob/average_speed # наработка в часах
    workout_in_days = workout_in_hours/motorhours_per_day
    workout_in_years = workout_in_days/workdays_per_year
    km_per_year = average_speed * motorhours_per_day * workdays_per_year
    srok = prob / km_per_year
# fullrun - полный пробег - он больше, чем prob (пробег на износ (workout)

# Топливо - fuel section
    fuel__cost_per_km = fuel__liters_per_km * fuel__cost_per_liter
    fuel__fullrun_cost = fuel__cost_per_km*prob/x_k  # это в случае среднего вождения (a=1)
    q_0 = fuel__fullrun_cost
    fuel__workout_cost = a*q_0*x_k # ревльная стоимость всего сожженого бензина за пробег до продажи авто
# прибавка расхода топлива за счет деградации двигателя к концу срока службы
    q_1 = q_0 * fuel__usage_increase_by_time_of_workout # коэффициент к концу срока службы
    fuel__usage_additional_cost_by_time_of_workout = q_1*ct.mlog(x_k,a)
    # q_1*mlog(x_k;a)
    # mlog = Application.WorksheetFunction.Ln(1 / (1 - a * xk))
    fuel__total_usage_cost = fuel__workout_cost + fuel__usage_additional_cost_by_time_of_workout
# сливы топлива
    fuel__stolen_fullrun_cost = fuel__stealing_rate * q_0
    d = fuel__stolen_fullrun_cost
    # ЕСЛИ(flagDut;d*x_k*accu;d*x_k)
    fuel__stolen_workout_cost = d*x_k*accu if flagDut else d*x_k

#  Риск поломки или ДТП
# без учета деградации двигателя
    r_0 = (repair__year_cost_new_car / km_per_year) * C0 # руб на срок службы
    repair__workout_cost_wo_degradation = a * r_0 * x_k  # за срок службы 
    # =a*r_0*x_k
# с учетом деградации двигателя Миша: вероятность разрушения двигателя при пробеге от 400 до 600 тысяч составляет 95%
# x_600 =x_k*N34/E6
    x_600 = x_k * 6e5 / prob
# x_400 =x_k*N35/E6
    x_400 = x_k * 4e5 / prob
#r_1 =I34*C0*(1-x_k)/(mlog(L34;a)-mlog(L35;a))
    r_1 = breaking_on_last_hundreds_probability * \
            C0 * (1 - x_k)/(ct.mlog(x_600,a) - ct.mlog(x_400,a))
    # =r_1*mlog(x_k;a)
    repair__degradational_cost_by_time_of_workout = r_1 * ct.mlog(x_k,a)
    repair__total_cost_by_workout = repair__workout_cost_wo_degradation+\
        repair__degradational_cost_by_time_of_workout

    # Сервис 
# без учета деградации двигателя  за срок службы 
    service__price_per_year = service__price_part_per_year * C0
# за срок службы    s_0 = I41*srok/x_k
    s_0 = service__price_per_year * srok / x_k
    # =a*s_0*x_k
    service__price_by_time_of_workout = a * s_0 * x_k

    # холодильник
    fridge__loss_chance = fridge_loss_probability if flagFrLoss else 0.0 # (flagFrLoss;0,05;0)
    # h_0 = I46*L46*12*srok/x_k   сумма штрафов за срок службы машины
    h_0 = fridge__spoil_fee * fridge__loss_chance * 12 * srok / x_k
    # Потери продуктов из-за разморозки     за срок службы 
    # ЕСЛИ(flagThermo;h_0*x_k*accu;h_0*x_k)
    fridge__spoil_cost_by_workout = h_0*x_k*accu if flagThermo else h_0*x_k
    logger.info("fridge__spoil_cost_by_workout\n%s" % (fridge__spoil_cost_by_workout,))
# Зарплата водителя 
    # z_0=I54*12*srok/x_k
    z_0 = driver__salary * 12 * srok / x_k
    # =a*z_0*x_k*(1+i)/(1+b)
    driver__salaries_by_workout= a*z_0*x_k*(1+i)/(1+b)

# Доходы от продажи отработавшей срок машины 
    # =C0*(1-a*x_k)
    workout__car_cost = C0*(1-a*x_k)

# Доходы от продажи работы машины
    # =I61*L61*prob
    k = work__cost_per_tkm * payload * prob
    # k*x_k/(1+b)
    work__cost_by_workout = k*x_k/(1+b)

# Расходы за срок службы
    # =СУММ(E2;E51;E14;E23;E29;E34;E40;E46;E55;E19)-E58
    workout_expenditure = (C0 + \
                           C_plus + \
                           fuel__total_usage_cost + \
                           fuel__stolen_workout_cost + \
                           repair__total_cost_by_workout + \
                           service__price_by_time_of_workout + \
                           fridge__spoil_cost_by_workout + \
                           driver__salaries_by_workout \
                            - workout__car_cost)
    workout_profit = (work__cost_by_workout - workout_expenditure)

# Стоимость системы мониторинга
    monitoring__setup_cost = 0.
    monitoring__setup_cost += monitoring__tracker_cost if flagTracker else 0.
    monitoring__setup_cost += monitoring__dut_cost if flagDut else 0.
    monitoring__setup_cost += monitoring__termometr_cost if flagThermo else 0.
    monitoring__setup_cost += monitoring__pp if flagPP else 0.
    monitoring__setup_cost += monitoring__block_eng_cost if flag_block_eng else 0.
    monitoring__setup_cost += monitoring__alarm_btn_cost if flag_alarm_btn else 0.
    # monitoring__setup_cost +=  if  else 0.
    monitoring__cost_by_workout = monitoring__setup_cost + \
                        monitoring__abonent_pays_per_month * 12 * srok

# Эффективность работы машины
    car_efficiency = work__cost_by_workout / workout_expenditure

# Среднемесячные показатели
    workout_expenditure_per_month = workout_expenditure / (12*srok)
    workout_profit_per_month = workout_profit / (12*srok)

    calc_results_dict['workout_profit'] = workout_profit
    calc_results_dict['work__cost_by_workout'] = work__cost_by_workout
    calc_results_dict['workout_expenditure_per_month'] = workout_expenditure_per_month
    calc_results_dict['workout_profit_per_month'] = workout_profit_per_month
    calc_results_dict['monitoring__setup_cost'] = monitoring__setup_cost
    calc_results_dict['monitoring__cost_by_workout'] = monitoring__cost_by_workout
    
    # все аддитивные величины домножить на число машин
    # (скидки делать здесь)
    calc_results_dict.update((x, y*cars_quantity) for x, y in calc_results_dict.items())
    
    calc_results_dict['car_efficiency'] = car_efficiency
    calc_results_dict['srok'] = srok
    return calc_results_dict

def compare(par_dict):
    # Сравнение выгоды без системы и с системой
    results_with_monitoring = calc(par_dict)
    logger.debug("results_with_monitoring['workout_profit']\n%s" % (results_with_monitoring['workout_profit'],))
    logger.debug("results_with_monitoring['car_efficiency']\n%s" % (results_with_monitoring['car_efficiency'],))

    # как будто мониторинга нет
    par_dict['i'] = accu # коэфф-т простоев !!! нигде не использвется! ввести.
    par_dict['b'] = accu # коэфф-т "левых" ходок
    par_dict['flagTracker'] = 0.  # ставим ли трекер
    par_dict['flagDut'] = 0. # устанавливается ли ДУТ
    par_dict['flagThermo'] = 0. # устанавливается ли термометр
    par_dict['flagFrLoss'] = 0. # портится ли товар без холодильника
    par_dict['flagI'] = 0. # есть ли контроль простоев (Idle)
    par_dict['flagPP'] = 0. # есть ли контроль пассажиропотока
    results_wo_monitoring = calc(par_dict)

    logger.debug("results_wo_monitoring['workout_profit']\n%s" % (results_wo_monitoring['workout_profit'],))
    logger.debug("results_wo_monitoring['car_efficiency']\n%s" % (results_wo_monitoring['car_efficiency'],))

    srok = results_with_monitoring['srok'] 

    monitoring__additional_profit = results_with_monitoring['workout_profit'] - \
                                     results_wo_monitoring['workout_profit']
    monitoring__additional_profit_per_month = monitoring__additional_profit / (12*srok)

    if monitoring__additional_profit != 0.:
        monitoring__recoupment = \
                results_wo_monitoring['monitoring__cost_by_workout'] \
                 / monitoring__additional_profit_per_month
    else:
        monitoring__recoupment = 0.
    results_with_monitoring['monitoring__recoupment'] = monitoring__recoupment
    results_with_monitoring['monitoring__additional_profit_per_month'] = monitoring__additional_profit_per_month
    # results_with_monitoring[''] = 
    return results_with_monitoring

if __name__ == '__main__':
    ct.setup_logging()
    d = ct.get_and_store_params()
    # d = read_params_dict(from_dropbox=True)
    print(d)
