from flask import jsonify,request,Response
from .. import main


from time import time


DAY_IN_SECONDS = 86400
TOKEN_DURATION = DAY_IN_SECONDS / 4

class AllFilters:

    """Treats an HTTP request to build the samples selection, pagination and variant filters
    according to the request's parameters."""
    def __init__(self, request, db):
        from ..filters.sort import sort_from_request
        from ..filters.pagination import pagination_from_request
        from ..filters.filters_factory import variant_filters_from_request, return_filters_to_view
        from varappx.stats.stats_service import stats_service

        """Extract filters etc. information from http request."""
        self.db = db
        self.sort = sort_from_request(request)
        self.pg = pagination_from_request(request)
        #self.ss = samples_selection_from_request(request, db)
        self.ss = None
        self.fc = variant_filters_from_request(request, db, self.ss)
        self.filterconfig = return_filters_to_view(request, db, self.ss)
        self.stats = stats_service(db)
        self.request=request

    #@timer
    def apply_all_filters(self):
        """Return a filtered and sorted variants collection."""
        # If the sorting field is in the db, use the db engine to sort.
        # Else, manage the case when the sorting field is added at expose time, after exposition...
         #with open('/home/liaoth/Desktop/debug.info', 'a+') as f1:
         #    f1.write('main views,apply_all_filters\n\n:')
         #   f1.write('self=%s ; request=%s \n' % (str(self), str(self.request.GET)))
        var = self.fc.apply(db=self.db,
            sort_by=self.sort.key, reverse=self.sort.reverse,
            limit=self.pg.lim, offset=self.pg.off)
        return var

    #@timer
    def expose(self):
        """Return a dict exposing variants, filters, stats etc. to be sent to the view."""
        from varappx.data_models.variants import expose_variant_full, annotate_variants
        t1 = time()
        filter_result = self.apply_all_filters()
        t2 = time()
        var = filter_result.variants
        stat = self.stats.make_stats(filter_result.ids)
        t3 = time()
        var = [expose_variant_full(v, self.ss) for v in var]
        t4 = time()
        var = annotate_variants(var, self.db)
        t5 = time()
        #logger.info("Apply/Stats/Expose/Annotate: {:.3f}s {:.3f}s {:.3f}s {:.3f}s".format(t2-t1, t3-t2, t4-t3, t5-t4))
        # TODO? How can one sort wrt. these fields?
        #if self.sort.key is not None and self.sort.key not in VARIANT_FIELDS:
        #    self.sort.sort_dict(var, inplace=True)
        response = {'variants': var}
        response["filters"] = [str(x) for x in self.fc.list]
        response["nfound"] = stat.total_count
        response["stats"] = stat.expose()
        response["FilterConfig"] = {}
        # TODO? fill suitable format of filterconfig in order to send to frontend to construct views.
        return response

#
def auto_process_OPTIONS(request):
    if request.method == 'OPTIONS':
        resp = Response('test')
        mime_res = {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Headers': 'x-requested-with, content-type, accept, origin, authorization, x-csrftoken',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
            'Access-Control-Max-Age': TOKEN_DURATION}
        for _k, _v in mime_res.items():
            resp.headers.setdefault(_k, _v)
        return resp


#
# def samples(request, db, user=None):
#     """Return a JSON with the list of Samples."""
#     ss = samples_selection_from_request(request, db)
#     return JsonResponse(ss.expose(), safe=False)
#
@main.route('/<db>/variants',methods=['OPTIONS','GET','POST'])
def variants(db, user=None):
    """Return a JSON with info on the requested Variants."""

    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    filters = AllFilters(request, db)
    response = filters.expose()
    return jsonify(response)

@main.route('/<db>/stats',methods=['OPTIONS','GET','POST'])
def stats(db, user=None):
    """Return a JSON with stats over the whole db (to query only once at startup)."""
    from varappx.stats.stats_service import stats_service
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    stat = stats_service(db).get_global_stats()
    #import pdb;pdb.set_trace()
    return jsonify(stat)
#
# @json_view
# def count(request, db, **kwargs):
#     """Return the total number of variants in the database.
#     Used for filling up the cache and REST tests.
#     """
#     n = Variant.objects.using(db).count()
#     response = HttpResponse(n)
#     return response
#
# @json_view
# def location_find(request, db, loc, **kwargs):
#     """Return an exposed GenomicRange for each location in the comma-separated list *loc*."""
#     locs = LocationService(db).find(loc)
#     locations = [l.expose() for l in locs]
#     return JsonResponse(locations, safe=False)
#
# @json_view
# def location_names_autocomplete(request, db, prefix):
#     """Return gene names starting with *prefix*."""
#     ans = LocationService(db).autocomplete_name(prefix, maxi=10)
#     return JsonResponse(ans, safe=False)
#
# @json_view
# def export_variants(request, db, **kwargs):
#     """Create a TSV file with the variants data and serve it."""
#     file_format = request.GET['format']
#     fields = request.GET.get('fields', '').split(',')
#     filters = AllFilters(request, db)
#     var = filters.apply_all_filters().variants
#     if file_format == 'report':
#         filename = 'varapp_report.txt'
#     else:
#         filename = 'variants.' + file_format
#     response = HttpResponse(content_type="text/plain")
#     response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
#     response['Access-Control-Expose-Headers'] = 'Content-Disposition'
#     response['Access-Control-Allow-Headers'] = 'Content-Disposition'
#     if file_format == 'txt':
#         #with open('/home/liaoth/tools/varapp_venv/testing.log','w') as f1:
#          #   f1.write(str((var, response, filters.ss, fields)))
#         export.export_tsv(var, response, filters.ss, fields)
#     elif file_format == 'vcf':
#         export.export_vcf(var, response, filters.ss)
#     elif file_format == 'report':
#         params = dict(request.GET)
#         export.export_report(var, response, db, params)
#     elif file_format == 'table':
#         export.export_tsv(var, response, filters.ss, fields)
#         #raise EnvironmentError
#
#     return response
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#



