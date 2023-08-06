define([],
    function () {
        return {
            // connection dialog
            connection: {
                name: null,
                dto: null,
                candidateName: null,
                candidateDTO: null
            },
            working_dir: null,
            working_dir_element: null,
            download_dir: null,

            // upload dialog
            uploadDataSetType: null,
            uploadDataSetTypes: {},
            uploadEntity: null,
            datasetCheckboxes: [],
            fileCheckboxes: [],
            selectedFiles: [],
            unselectedDatasets: [],

            // download dialog
            selectedDatasets: new Set([]),
            entity: null,

            // openBIS v3 connection
            openbisService : null
        }
    }
)