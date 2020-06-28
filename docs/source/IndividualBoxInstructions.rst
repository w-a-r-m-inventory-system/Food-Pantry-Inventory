###########################
Individual Box Instructions
###########################

After logging in click on the blue **Manual Box and Pallet Maintence** button as shown
below to begin processing a box or a pallet. You will be directed to the
**Manual Box and Pallet Management** screen.

.. image:: manual_box_images/ManualBoxStart_0_00_06.png


Manual Box and Pallet Management Screen
++++++++++++++++++++++++++++++++++++++++

To manage a pallet manually click on the **Manage a pallet manually** link.
**Add screen here showing where to click. Currently the user documentation is not
implmented for this section.**

To manage individual boxes of product click on the **Manage an individual box manually**
link as shown below.

.. image:: manual_box_images/ManageManualBox_0_00_19.png

Manual Pallet Management Screens
++++++++++++++++++++++++++++++++

**Add screen here showing where to click for manual Pallet Management. Also this
section should include Manual Pallet Management Screens**

Manual Box Management Screens
+++++++++++++++++++++++++++++

If you clicked on the **Manage an individual box manually** link you should be
directed to the **Manual Box Management** screen.
Here you will see 5 menu items.

+ **Check the status of a box**
+ **Add a new box to inventory**
+ **Checkin a new box**
+ **Checkout (consume product in) a box**
+ **Move a box**

.. image:: manual_box_images/ManualBox5Items_0_00_30.png

Of course you can also **Return to manual menu**. Each of the 5 menu items will be discussed
below.

|

Manual Status a Box Screen
============================

From Manual Box Management clicking on **Check the status of a box** will bring you to the
**Manual Status a Box** screen. Here you can check th box status by entering a 5 digit
box number and then clicking on the **Search** button.

.. image:: manual_box_images/ManualStatusABox_0_01_01.png

After clicking on the **Search** button you should see a screen listing the Box Number,
Box Type, Box Contents, Contents Expire (expiration date) and location- Row, Bin and Tier
number.

.. image:: manual_box_images/ManualStatusABox_0_01_06.png

From this screen you can click on **Check another box** or **Return to Manual Box Menu**.

|

New Box Screen
================

With this screen you can add a new box following the 4 steps listed below.

    (1) Enter a 5 digit box number.
    (2) Click on the drop down list triangle at the far right.
    (3) Choose an item from the drop down list.
    (4) Finally click on the **Add Box** button (hidden from view in the below graphic).

.. image:: manual_box_images/AddNewBox_0_00_58.png

After clicking on **Add Box** you should see the following screen. From there you can
**Add another box** or **Return to Manual Box Menu** by clicking on the links in the
**New Box** screen.

.. image:: manual_box_images/AddNewBoxSuccess_0_01_05.png

If there was an error you will see the following screen. Simply click on **Cancel Adding
a Box** to return to the **Manual Box Management** screen.

.. image:: manual_box_images/AddNewBoxFailure_0_01_14.png

|

Checkin a Box Screen
=====================

With this screen you can add all the information needed to check in a box of food
items to warehouse inventory. The blank **Checkin Box** screen is shown below.

.. image:: manual_box_images/CheckinBox_0_01_26.png

The first two items to enter are the **Box number** and **Product**. With the keyboard
enter a 5 digit 'Box number' in the **Box number** field. Then click on the small
triangle int the circle at the right of the **Product** drop down list to select a
product with your mouse.

.. image:: manual_box_images/CheckinBoxSelectProduct_0_01_31.png

After entering the **Product** the next step is to  enter the pallet location.
You will have to select 3 different entries with your mouse.

    (1) Row number
    (2) Bin number ( Bin number in the length of a row)
    (3) Tier number (level up or down

Each entry uses a drop down list and you will make a choice from the drop down list.
In the graphic below the **Row** and **Bin** numbers have been chosen and the drop down
list is shown with the **Tier** number.

.. image:: manual_box_images/CheckinBoxLocation_0_01_49.png

After entering the location enter the expiration year by clicking on the small triangle
to the right of the **Exp year** field and making a selection from the drop down list.

.. image:: manual_box_images/CheckinBoxExpYear_0_01_55.png

The last selection you will have to make is the expiration month. There are 2 drop down
list fields here **Exp month start** and **Exp month end**. These fields are optional and
it is not necessary to fill these fields out. These drop down lists show a list of all
the months in the year. You can also choose to **only** fill out the **Exp month start**
field also. However if you choose to fill out the **Exp month end** field you must make
sure it is a later month in the year than the **Exp month start** field. So if you enter
**April** in the **Exp month start** field, then you must enter **May** or a later month
in the **Exp month end** field.

When you are through with the **Exp month** fields click on the blue **Set Box Checkin
Information** button to enter all the Checkin data.

.. image:: manual_box_images/CheckinBoxExpMonth_0_02_08.png

If everything has worked correctly you should see the following screen below. Simply click
on the **Return to Manual Box Menu** link to continue.

.. image:: manual_box_images/CheckinBoxSuccess_0_02_12.png

If there is an error you should see a screen like the one below. The
red arrows point to what has to be fixed before a box can be Checked in. Click on the
**Cancel Box Checkin** link at the bottom of the page to go back to the **Manual Box
Management** screen to start over.

.. image:: manual_box_images/CheckinBoxFailure_0_03_05.png

|

Consume (Empty) a Box Screen
=============================

To consume or empty a box enter a 5 digit box number in the **Box Number** field. Then
click on the blue **Search** button.

.. image:: manual_box_images/ConsumeBox_0_03_15.png

If everything went ok you should see the box information on the next screen. The box
information includes the Box Number, the Box Type, the Box Contents, the year the
Contents Expire and the location- Row, Bin, Tier. Click on the blue **Consume** button
to continue if all the information seems correct.

.. image:: manual_box_images/ConsumeBoxMessage_0_03_22.png

The next screen should contain a message stating that a box 'has been succesfully
consumed'. Click on the **Return to Manual Box Menu** link to return to the **Manual
Box Management** page.

.. image:: manual_box_images/ConsumeBoxSuccess_0_03_22.png

In case of error you should see a screen similar to the one below listing the error.
Click on the **Cancel Box Consumption** link to return to the **Manual Box Management**
page.

.. image:: manual_box_images/ConsumeBoxFailure_0_03_40.png



Move Box Screen
================

To move a box to a different pallet enter the 5 digit box number in the **Box Number**
field and then click on the blue **Search** button.

.. image:: manual_box_images/MoveBox_0_03_55.png

The next **Move Box** screen contains all the box information. In this screen
you can choose a new location by entering new **Row**, **Bin**, **Tier** locations. Click
on the small triangle to the right of each **Row**, **Bin**, **Tier** to get your drop down
list choices. After choosing your new location entries click on the blue **Move**
button to change the information in the database.

.. image:: manual_box_images/MoveBoxFillIn_0_04_19.png

If there are no errors you should see a screen similar to the one below. Click on the
**Return to Manual Box Menu** link to return to the **Manual Box Management**
screen.

.. image:: manual_box_images/MoveBoxSuccess_0_04_23.png

In case of error you will see a screen similar to the one below with an error message.
Click onthe **Cancel Box Move** link to return to the **Return to Manual Box Menu**.

.. image:: manual_box_images/MoveBoxFailure_0_04_32.png
