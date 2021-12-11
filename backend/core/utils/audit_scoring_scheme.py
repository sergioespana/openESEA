def calculate_scoring_scheme():
    print('yeeee')
    return True

    '''
    ii1 1 ( 0.6 * ii2 + 0.4 * ii3)
        absolute_weights: [ii2: 0.6, ii3: 0.4, ii4: 0,15, ii5: 0,45, ii6: 0,24]
        sorted_weights: [ii2: 0.6, , ii5: 0.45, ii3: 0.4, ii6: 0.24, ii4: 0.15]
    - ii2 0.6 (0.25 * ii4 + 0.75 * ii5)
        absolute_weights: [ii4: 0.25, ii5: 0.75]
        sorted_weights: [ii5: 0.75, ii4: 0.25]
        - ii4 0.25
        - ii5 0.75
    - ii3 0.4 (if company_size > 100 then (0.4 * ii6) else (0.6 * ii6))   --> e.g company_size = 60
        absolute_weights: [ii6: 0.6]
        ii6
    
    # ii7 1 (0.2 * ii2)
    # - ii2 0.2
    '''