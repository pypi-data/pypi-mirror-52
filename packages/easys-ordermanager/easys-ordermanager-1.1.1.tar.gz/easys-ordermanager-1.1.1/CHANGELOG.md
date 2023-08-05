# Changelog


## 1.1.1 (2019-09-06)
Small fix on pep8 error

## 1.1.0 (2019-09-04)

This release contains backwards incompatible changes


* Split Display detail OrderLineDisplaySerializer in two different serializers and fields for basic and premium product levels:
  * remove `detail_display` field from `OrderLine` 
  * add `detail_display_basic` field (`OrderLineDisplayBasicSerializer`) on `OrderLine`  
   
     The serializer contains following fields:  
     
     New fields:
       * `banner_color_selection`  
         choice field with values: 1 for _Color from Logo/Website_ and 2 for _Set color_ . To be used in combination with fields `color_code_x`  
     
     Fields with changed definition
       * `impressions_per_month`  
         choice field with accepted values: 20.000 , 40.000 and 80.000
       * `creative_options`  
         choice field contains only values: 1 for _Customer provided_ and 3 for _Create animated_
     
     Fields with the same definition as in the previous OrderLineDisplaySerializer
       * `geo_targeting`
       * `geo_targeting`
       * `campaign_goal`
       * `headline`
       * `sub_headline`
       * `bullet_points`
       * `call_to_action`
       * `color_code_1`
       * `color_code_2`
       * `color_code_3`
       * `stock_images_allowed`
       * `target_page_type`
       * `target_url`
       * `package_template`
       * `location_frame_text`
       * `creative_options`
      
  * add `detail_display_premium` field (`OrderLineDisplayPremiumSerializer`) on `OrderLine`   
   
     Serializer contains following fields with the same definition as in the previous OrderLineDisplaySerializer
       * `booking_type`
       * `target_devices`
       * `creatives_format`
       * `impressions_per_day`
       * `impressions_per_month`
       * `age_targeting`
       * `gender_targeting`
       * `geo_targeting`
       * `channel_targeting`
       * `interest_targeting`
       * `campaign_goal`
       * `target_page_type`
       * `target_url`
       * `creative_options`
      

* Split Google Ads detail OrderLineGoogleAdsSerializer in two different serializers for basic and premium product levels:
  * remove `detail_google_ads` field from `OrderLine`     
  * add `detail_google_ads_basic` field (`OrderLineGoogleAdsBasicSerializer`) on `OrderLine`  

       Serializer contains following fields with the same definition as in the previous OrderLineGoogleAdsSerializer
    * `campaign_goal`
    * `regions`
    * `expected_impression_share`
    * `keywords`
    * `keywords_with_zero_search_volume`
    * `target_audience`

  * add `detail_google_ads_premium` field (`OrderLineGoogleAdsPremiumSerializer`) on `OrderLine`  

       Serializer contains following fields with the same definition as in the previous OrderLineGoogleAdsSerializer
     * `call_to_action`
     * `campaign_goal`
     * `regions`
     * `expected_clicks`
     * `expected_conversions`
     * `existing_account_id`
     * `include_remarketing`
     * `keywords`
     * `keywords_with_zero_search_volume`
     * `target_audience`
     * `usp`


* All product fee fields on `OrderLineSerializer` became optional:
  * `setup_fee`
  * `start_fee`
  * `budget`
  * `fee`
  * `one_time_budget`
  * `commission`
  * `deferred_payment_sum`

* Add validation for commission provided for product type Google Ads level Basic: fixed value of 40  
* Add validation for combination of product type and level: check if a matching HC products subtype exists
* Add validation for the payment fees provided: check if a matching HC payment type exists.


## 1.0.4 (2019-08-21)

* Add new fee type postponed_setup_fee
* Add reference customer boolean to Location serializer

## 1.0.3 (2019-07-03)

* Don't use allow_null with BooleanField (`djangorestframework<3.9` doesn't support it)


## 1.0.2 (2019-07-01)

* Allow to use empty/null values for non-required fields


## 1.0.1 (2019-06-27)

* Add missing files to the package


## 1.0.0 (2019-06-24)

* Initial release
