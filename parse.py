import re

def parse_jsp_instances(file_path):
    """
    Parses a text file containing JSP instances into a dictionary.
    Structure: { 'instance_name': { 'n_jobs': int, 'n_machines': int, 'jobs': [[(m, t), ...], ...] } }
    """
    instances = {}
    
    with open(file_path, 'r') as f:
        content = f.read()

    # Split the file by the "instance" keyword
    raw_instances = re.split(r'\s*\+{5,}\s*instance\s+', content)

    for section in raw_instances:
        if not section.strip() in section: # Skip empty or header sections
            continue
            
        lines = [line.strip() for line in section.split('\n') if line.strip()]
        
        # Extract Instance Name
        instance_name = lines[0]
        
        # Find the line containing job and machine counts
        dims_index = -1
        for i, line in enumerate(lines):
            if re.match(r'^\d+\s+\d+$', line):
                dims_index = i
                break
        
        if dims_index == -1:
            continue

        n_jobs, n_machines = map(int, lines[dims_index].split())
        
        # Parse job data
        job_data = []
        for i in range(dims_index + 1, dims_index + 1 + n_jobs):
            values = list(map(int, lines[i].split()))
            
            # Group into (machine, time) pairs
            tasks = [(values[j], values[j+1]) for j in range(0, len(values), 2)]
            job_data.append(tasks)
            
        instances[instance_name] = {
            'n_jobs': n_jobs,
            'n_machines': n_machines,
            'jobs': job_data
        }

    return instances