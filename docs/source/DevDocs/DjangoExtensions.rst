#################
Django Extensions
#################

One of the libraries included in this project is django-extensions
(https://django-extensions.readthedocs.io/).  It has a number of useful
extension to the manage.py module provided by Django.  The extensions used
by this project are:

Model Relationships
    This extention produces a graph of the tables in the application and
    their interrelationships.  More details are provided in
    `Model (Table) Relationships <graph_models_>`_ below.

Model vs. Database Differences
    This extension produces output that shows if your models and database
    schema are in sync.  If not, it outputs the SQL statements that will put
    it in sync.  See `Model vs. Database Differences <sqldiff>`_ below for
    an example.

Show all URLs
    This extension is useful to show all defined URL's, the view associates
    with each URL, and the name attached to that URL.  See
    `Show URLs <show_urls>`_ below.

Dump Script
    A extension is available to dump the entire schema and all data to a
    Python script.  See `Dump Script <dumpscript>`_ below.

Dump Data
    The dump data command can dump the contents of a table in a format
    suitable as a fixture file.  See `Dump Data <dumpdata>`_ below.

.. _graph_models:

***************************
Model (Table) Relationships
***************************

The extension "graph-models" generates a graph showing all the models
(tables) defined and how they are related.  Each foreign key is shown with
an arrow pointing to the source table and field.  The arrows indicate if the
relationship is one-to-one, one-to-many or many-to-many.

A graph for this project can be downloaded from

.. only:: builder_html

    :download:`Inventory and Authorization Models
    <InventoryProjectModelsGrouped.pdf>`

This extension generatss a ".dot" file that is interpreted by the GraphViz
library (see `GraphViz documentation <http://www.graphviz.org/>`_ ).

By also loading the library PyGraphViz (see
`PyGraphViz documentation <http://pygraphviz.github.io/index.html>`_) the "
.dot" file generated above is converted into a format usable for humans.

The command used to make all this happen is::

    ./manage.py graph_models fpiweb auth -g -o InventoryProjectModelsGrouped.pdf

.. _sqldiff:

******************************
Model vs. Database Differences
******************************

This extension shows any difference between the models and the database.

The command::

    ./manage.py sqldiff -a -e

produced this output::

    BEGIN;
    -- Application: fpiweb
    -- Model: Activity
    DROP INDEX "fpiweb_activity_BoxNumber_10d7ca04_like";
    -- Model: Constraints
    ALTER TABLE "fpiweb_constraints"
            ADD CONSTRAINT "fpiweb_constraints_constraint_name_0fa0e463_uniq" UNIQUE ("constraint_name");
    CREATE INDEX "fpiweb_constraints_constraint_name_0fa0e463_like"
            ON "fpiweb_constraints" ("constraint_name" varchar_pattern_ops);
    COMMIT;

This command reported the result as text rather than SQL.  ::

    ./manage.py sqldiff -a -e -t

Results::

    + Application: fpiweb
    |-+ Differences for model: Activity
    |--+ field 'fpiweb_activity_BoxNumber_10d7ca04_like' INDEX defined in database schema but missing in model
    |-+ Differences for model: Constraints
    |--+ field 'constraint_name' UNIQUE named 'fpiweb_constraints_constraint_name_0fa0e463_uniq' defined in model but missing in database
    |--+ field 'constraint_name' INDEX named 'fpiweb_constraints_constraint_name_0fa0e463_like' defined in model but missing in database

.. _show_urls:

******************************
Show URLs
******************************

The "show_urls" command is not as polished as the other commands although it
still produces useful output.

The command::

    ./manage.py show_urls

produces output like this (partial)::

    /       fpiweb.views.LoginView
    /fpiweb/        fpiweb.views.IndexView  fpiweb:index
    /fpiweb/about/  fpiweb.views.AboutView  fpiweb:about
    /fpiweb/activity/download/      fpiweb.views.ActivityDownloadView       fpiweb:download_activities
    /fpiweb/box/<int:pk>/   fpiweb.views.BoxDetailsView     fpiweb:box_details
    /fpiweb/box/<int:pk>/edit/      fpiweb.views.BoxEditView        fpiweb:box_edit
    /fpiweb/box/<int:pk>/empty/     fpiweb.views.BoxEmptyMoveView   fpiweb:box_empty
    /fpiweb/box/<int:pk>/empty_move/        fpiweb.views.BoxEmptyMoveView   fpiweb:box_empty_move
    /fpiweb/box/<int:pk>/fill/      fpiweb.views.BoxEmptyMoveView   fpiweb:box_fill
    /fpiweb/box/<int:pk>/move/      fpiweb.views.BoxMoveView        fpiweb:box_move
    /fpiweb/box/box<int:number>/    fpiweb.views.BoxScannedView     fpiweb:box_scanned
    /fpiweb/box/box_form/   fpiweb.views.BoxItemFormView    fpiweb:box_form
    /fpiweb/box/new/<str:box_number>/       fpiweb.views.BoxNewView fpiweb:box_new
    /fpiweb/build_pallet/   fpiweb.views.BuildPalletView    fpiweb:build_pallet
    /fpiweb/build_pallet/   fpiweb.views.BuildPalletView    fpiweb:build_pallet
    /fpiweb/build_pallet/<int:box_pk>/      fpiweb.views.BuildPalletView    fpiweb:build_pallet_add_box
    /fpiweb/build_pallet/<str:box_number>/  fpiweb.views.BuildPalletView    fpiweb:build_pallet_add_box
    /fpiweb/constraint/add/ fpiweb.views.ConstraintCreateView       fpiweb:constraint_new
    /fpiweb/constraint/delete/<int:pk>/     fpiweb.views.ConstraintDeleteView       fpiweb:constraint_delete
    /fpiweb/constraint/edit/<int:pk>/       fpiweb.views.ConstraintUpdateView       fpiweb:constraint_update
    /fpiweb/constraints/    fpiweb.views.ConstraintsListView        fpiweb:constraints_view
    /fpiweb/index/  fpiweb.views.IndexView  fpiweb:index
    /fpiweb/loc_bin/        fpiweb.views.LocBinListView     fpiweb:loc_bin_view
    /fpiweb/loc_bin/add/    fpiweb.views.LocBinCreateView   fpiweb:loc_bin_new
    /fpiweb/loc_bin/delete/<int:pk>/        fpiweb.views.LocBinDeleteView   fpiweb:loc_bin_delete
    /fpiweb/loc_bin/edit/<int:pk>/  fpiweb.views.LocBinUpdateView   fpiweb:loc_bin_update
    /fpiweb/loc_row/        fpiweb.views.LocRowListView     fpiweb:loc_row_view
    /fpiweb/loc_row/add/    fpiweb.views.LocRowCreateView   fpiweb:loc_row_new
    /fpiweb/loc_row/delete/<int:pk>/        fpiweb.views.LocRowDeleteView   fpiweb:loc_row_delete
    /fpiweb/loc_row/edit/<int:pk>/  fpiweb.views.LocRowUpdateView   fpiweb:loc_row_update
    /fpiweb/loc_tier/       fpiweb.views.LocTierListView    fpiweb:loc_tier_view
    /fpiweb/loc_tier/add/   fpiweb.views.LocTierCreateView  fpiweb:loc_tier_new
    /fpiweb/loc_tier/delete/<int:pk>/       fpiweb.views.LocTierDeleteView  fpiweb:loc_tier_delete
    /fpiweb/loc_tier/edit/<int:pk>/ fpiweb.views.LocTierUpdateView  fpiweb:loc_tier_update
    /fpiweb/login/  fpiweb.views.LoginView  fpiweb:login
    /fpiweb/logout/ fpiweb.views.LogoutView fpiweb:logout
    /fpiweb/maintenance/    fpiweb.views.MaintenanceView    fpiweb:maintenance
    /fpiweb/manual_add_box/ fpiweb.views.ManualNewBoxView   fpiweb:manual_add_box
    /fpiweb/manual_box_status/      fpiweb.views.ManualBoxStatusView        fpiweb:manual_box_status
    ...

The output has the URL, the view it invokes, and the name attached to it.
The output has a tab character between each field so it could be imported
into a spreadsheet for easy reference and manipulation.  At this point in
our development, run the command to get the current list of URL's.

.. _dumpscript:

***********
Dump Script
***********

The "dumpscript" command will dump all the schema and data from the current
database into a script.  The script can subsequently be used to reload into
a database that was just created.  The script will create the schema for the
application (and other Django tables) and load all the previously known data
into it.  The advantage of the script vs. a database backup is that the
script is completely in python so there are no SQL syntax details get in the
way of moving to a different database vendor.

Unfortunately, this extension chokes on our database because we have "time
zone aware" data in it.  Perhaps we can file an issue with the maintainers
and get a fix or workaround.

.. _dumpdata:

*********
Dump Data
*********

The "dumpdata" command can be used to create a file suitable for inclusion
in the fixtures directory.  Once the table has all the desired records and
values, use a command similar to the one below.  ::

    ./manage.py dumpdata  -o pallot.json fpiweb.pallet

This command is an example of dumping the fpiweb pallet table to a file
called pallet.json in the current directory.  It can then be moved to the
fixtures directory or other desired location.

(more Django extensions used by this project)
