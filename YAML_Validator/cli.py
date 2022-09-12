import click
import yaml
from bg_atlasapi.bg_atlas import BrainGlobeAtlas

@click.command()
#@click.option('--file_name', '-c', is_flag=True, help='Relative or absolute path to a file.')
@click.argument('file_name', default=None)
def main(file_name):
    """Validates a YAML file"""
    click.echo(f'Processing file: {file_name}')
    yaml_file = get_yaml_file(file_name)
    if not yaml_file:
        click.echo('File provided is invalid')
        return
    atlas = get_atlas()
    invalid_key_info = check_if_target_location_has_invalid_entry(yaml_file, atlas)
    validation_message = 'targeted_location has NO invalid entry' if len(invalid_key_info) == 0 else 'targeted_location has invalid entries'
    click.echo(validation_message)

def check_if_target_location_has_invalid_entry(yaml_file, atlas):
    """
    Check if targe location has an invalid entry

    Parameters
    ----------
    yaml_file : dict
        Yaml file content
    atlas : Bg_atlasapi.bg_atlas.BrainGlobeAtlas
        atlas object contain valid brain entries
    """
    validation_failures = []
    for index, electrode_group in enumerate(yaml_file['electrode_groups']):
        value = electrode_group['targeted_location']
        try:
            assert atlas.structures[value]
        except KeyError as error:
            validation_failures.append({
                'index': index,
                'key': 'target_location',
                'invalid_value': value,
                'exception': error,
            })
    return validation_failures

def get_atlas():
    """
    Read in the brain atlas for Sprague-Dawley
    """
    rat_code = 'whs_sd_rat_39um'
    atlas = BrainGlobeAtlas(rat_code, check_latest=False)
    return atlas

def get_yaml_file(file_name):
    """
    Read in yaml file

    Parameters
    ----------
    file_name : string
        Relative or absolute path to yaml file

    Returns
    -------
    dict
        yaml file
    """
    if not file_name:
        return None
    yaml_file = None
    with open(file_name) as file:
        yaml_file = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_file


if __name__ == '__main__':
    main()
